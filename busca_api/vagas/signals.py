from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import DecisaoVaga
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@receiver(pre_save, sender=DecisaoVaga)
def decisaovaga_pre_save(sender, instance, **kwargs):
    """
    Antes de salvar, tentamos buscar o objeto antigo (se existir) para comparar status.
    Se o status mudar de != 'Aprovada' para 'Aprovada', marcamos um flag no instance.
    """
    # Marca padrão
    instance._enqueue_scraping = False

    if not instance.pk:
        # criação nova: se já está aprovado no create, set flag
        if getattr(instance, 'status', None) == 'Pendente':
            # não enfileirar
            instance._enqueue_scraping = False
        elif getattr(instance, 'status', None) == 'Aprovada':
            instance._enqueue_scraping = True
        return

    try:
        old = DecisaoVaga.objects.get(pk=instance.pk)
    except DecisaoVaga.DoesNotExist:
        # criado novo (tratado acima)
        return

    old_status = getattr(old, 'status', None)
    new_status = getattr(instance, 'status', None)

    if old_status != new_status and new_status == 'Aprovada':
        instance._enqueue_scraping = True
    else:
        instance._enqueue_scraping = False

@receiver(post_save, sender=DecisaoVaga)
def decisaovaga_post_save(sender, instance, created, **kwargs):
    """
    Após salvar, se o flag pre_save definiu que devemos enfileirar, chamamos a task.
    """
    enqueue = getattr(instance, '_enqueue_scraping', False)
    if enqueue:
        # Import local para evitar circular imports
        from .tasks import scraping_task
        vaga_id = instance.vaga.id if instance.vaga_id is not None else None
        if vaga_id is None:
            logger.error("DecisaoVaga salva com enqueue=True mas sem vaga relacionada.")
            return
        # enfileira task assincronamente
        scraping_task.delay(vaga_id)
        logger.info(f"Scraping task enfileirada para vaga_id={vaga_id} via DecisaoVaga id={instance.id}")
