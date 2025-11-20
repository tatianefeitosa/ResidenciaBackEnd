from celery import shared_task
from celery.utils.log import get_task_logger
from vagas.models import Vaga
from vagas.scraping.github_scraper import run_github_scraping

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def scraping_task(self, vaga_id):
    """
    Task que dispara o scraping para uma vaga específica.
    Atualmente executa o GitHub Scraper.
    """
    try:
        vaga = Vaga.objects.get(id=vaga_id)

        requisitos = vaga.get_all_requirements_as_list()

        logger.info(f"Iniciando GitHub scraping para vaga_id={vaga_id}")

        run_github_scraping(vaga, requisitos)

        logger.info(f"Scraping task concluída para vaga_id={vaga_id}")

    except Exception as exc:
        logger.exception(f"Erro na scraping_task vaga_id={vaga_id}: {exc}")
        raise self.retry(exc=exc)
