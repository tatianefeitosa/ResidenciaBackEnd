# vagas/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from vagas.models import Vaga
from candidatos.models import Candidato, FonteBusca, CandidatoFonteBusca
from vagas.scraping.github_scraper import scrape_top_candidatos

import hashlib

logger = get_task_logger(__name__)

def make_source_hash(platform: str, unique_id: str):
    """Garante hash consistente para cada candidato."""
    s = f"{platform}:{unique_id}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def scraping_task(self, vaga_id, top_n=5):
    """
    Task responsável por executar o scraping GitHub para uma vaga específica
    e persistir os top N candidatos no banco.
    """
    try:
        vaga = Vaga.objects.get(id=vaga_id)

        logger.info(f"[SCRAPING] Coletando requisitos da vaga {vaga_id}...")
        requisitos = vaga.get_all_requirements_as_list()
        logger.info(f"[SCRAPING] Requisitos detectados: {requisitos}")

        logger.info(f"[SCRAPING] Iniciando GitHub Scraper para vaga {vaga_id}...")
        candidatos_brutos = scrape_top_candidatos(vaga, requisitos, top_n=top_n)
        logger.info(f"[SCRAPING] Scraper retornou {len(candidatos_brutos)} candidatos preliminares.")

        if not candidatos_brutos:
            logger.info(f"[SCRAPING] Nenhum candidato encontrado para vaga {vaga_id}.")
            return

        for cand in candidatos_brutos:
            source_hash = make_source_hash("github", cand["source_id"])

            # Persistir candidato
            candidato_obj, created = Candidato.objects.update_or_create(
                source_id_hash=source_hash,
                vaga=vaga,
                defaults={
                    "nome_candidato": cand["nome"],
                    "resumo_profissional": cand.get("resumo_profissional", ""),
                    "compatibilidade": float(cand.get("similarity_score", 0) * 100),
                    "raw_result": cand.get("raw_result", {}),
                    "habilidades_tecnicas": cand.get("habilidades_tecnicas", []),
                    "habilidades_interpessoais": cand.get("habilidades_interpessoais", []),
                    "diplomas": cand.get("diplomas", []),
                    "certificacoes": cand.get("certificacoes", []),
                    "idiomas": cand.get("idiomas", []),
                    "empresas": cand.get("empresas", []),
                    "localizacoes": cand.get("localizacoes", []),
                    "emails": cand.get("emails", []),
                    "telefones": cand.get("telefones", []),
                }
            )

            # Persistir fonte de busca
            url_perfil = cand.get("url_perfil")
            if url_perfil:
                fonte, _ = FonteBusca.objects.get_or_create(nome_site=cand.get("fonte_nome", "GitHub"),
                                                            url_perfil=url_perfil)
                CandidatoFonteBusca.objects.get_or_create(candidato=candidato_obj, fonte=fonte)

        logger.info(f"[SCRAPING] Top {len(candidatos_brutos)} candidatos persistidos para vaga {vaga_id}.")

    except Exception as exc:
        logger.error(f"[SCRAPING] Erro durante scraping da vaga {vaga_id}: {exc}", exc_info=True)
        raise self.retry(exc=exc)
