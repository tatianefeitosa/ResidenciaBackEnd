# candidatos/services.py (exemplo minimal)
from vagas.models import Vaga
from candidatos.models import FonteBusca, Candidato, CandidatoFonteBusca
from django.db import transaction

def run_scraping_for_vaga(vaga_id):
    vaga = Vaga.objects.get(pk=vaga_id)
    # Exemplo simples: apenas registra que foi chamada (substituir por scrapers reais)
    fonte, _ = FonteBusca.objects.get_or_create(nome_site='ExemploScraper')
    # criar candidato dummy apenas para teste (remova depois)
    with transaction.atomic():
        c = Candidato.objects.create(
            nome_candidato=f"Teste para vaga {vaga.nome_cargo}",
            vaga=vaga,
            compatibilidade=0.0,
            source_id_hash=f"test-{vaga_id}"
        )
        CandidatoFonteBusca.objects.create(candidato=c, fonte=fonte)
