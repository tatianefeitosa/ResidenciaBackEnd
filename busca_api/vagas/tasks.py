from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def scraping_task(self, vaga_id):
    """
    Task que orquestra o scraping para a vaga. Chama a função do serviço de candidatos.
    A função concreta run_scraping_for_vaga deve ser implementada em candidatos.services.
    """
    try:
        # import local para evitar circular imports na inicialização
        from candidatos.services import run_scraping_for_vaga
        run_scraping_for_vaga(vaga_id)
        logger.info(f"Scraping task concluída para vaga_id={vaga_id}")
    except Exception as exc:
        logger.exception(f"Erro na scraping_task vaga_id={vaga_id}: {exc}")
        # requeue com retry automático
        raise self.retry(exc=exc)
