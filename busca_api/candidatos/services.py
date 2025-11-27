'''import os
import hashlib
import requests
from django.db import transaction
from dotenv import load_dotenv

from vagas.models import Vaga, HabilidadeTecnica
from candidatos.models import (
    FonteBusca,
    Candidato,
    CandidatoFonteBusca,
    CandidatoHabilidadeTecnica
)

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}


# --------------------------
#  UTILITÁRIOS
# --------------------------

def gerar_hash_id(valor: str) -> str:
    return hashlib.sha256(valor.encode("utf-8")).hexdigest()


def calcular_compatibilidade(requisitos, bio, repos):
    """
    Compatibilidade: % de requisitos encontrados na bio + nomes de repositórios + descrições.
    """
    if not requisitos:
        return 0.0

    texto = (bio or "").lower()
    for r in repos:
        texto += " " + (r.get("name", "") or "").lower()
        texto += " " + (r.get("description", "") or "").lower()

    total = len(requisitos)
    encontrados = 0

    for req in requisitos:
        if req.lower() in texto:
            encontrados += 1

    return round((encontrados / total) * 100, 2)


# --------------------------
#  SCRAPER PRINCIPAL
# --------------------------

def github_buscar_usuarios(requisitos):
    """Consulta /search/users?q=skill+in:bio+in:login"""
    if not requisitos:
        return []

    # monta query: python in:bio OR django in:login ...
    query_parts = [f"{req} in:bio" for req in requisitos]
    query = "+".join(query_parts)

    url = f"https://api.github.com/search/users?q={query}&per_page=20"

    resp = requests.get(url, headers=GITHUB_HEADERS)
    resp.raise_for_status()

    return resp.json().get("items", [])


def github_detalhar_usuario(username):
    """Busca detalhes do usuário (bio, email, repos, local, nome)."""
    u_url = f"https://api.github.com/users/{username}"
    r_url = f"https://api.github.com/users/{username}/repos?per_page=50"

    u = requests.get(u_url, headers=GITHUB_HEADERS)
    repos = requests.get(r_url, headers=GITHUB_HEADERS)

    if u.status_code != 200:
        return None

    return {
        "perfil": u.json(),
        "repos": repos.json() if repos.status_code == 200 else []
    }


# --------------------------
#  SALVAR NO BANCO
# --------------------------

@transaction.atomic
def salvar_candidato_github(vaga, dados, requisitos):
    """Salva um candidato real no banco."""
    perfil = dados["perfil"]

    username = perfil.get("login")
    nome = perfil.get("name") or username
    bio = perfil.get("bio")
    repos = dados["repos"]

    # hash único: "github:username"
    hash_id = gerar_hash_id("github:" + username)

    # evita duplicações
    candidato, created = Candidato.objects.get_or_create(
        source_id_hash=hash_id,
        defaults={
            "nome_candidato": nome,
            "resumo_profissional": bio,
            "vaga": vaga,
            "raw_result": dados,
        }
    )

    # sempre recalcula compatibilidade
    candidato.compatibilidade = calcular_compatibilidade(requisitos, bio, repos)
    candidato.save()

    # fonte de busca
    fonte, _ = FonteBusca.objects.get_or_create(nome_site="GitHub")

    CandidatoFonteBusca.objects.get_or_create(
        candidato=candidato,
        fonte=fonte
    )

    # vincula as habilidades técnicas encontradas
    for req in requisitos:
        skill = HabilidadeTecnica.objects.filter(nome__iexact=req).first()
        if skill:
            CandidatoHabilidadeTecnica.objects.get_or_create(
                candidato=candidato,
                habilidade=skill
            )

    return candidato


# --------------------------
#  PIPELINE PRINCIPAL
# --------------------------

def run_scraping_for_vaga(vaga_id):
    vaga = Vaga.objects.get(pk=vaga_id)

    # coleta de requisitos técnicos da vaga
    requisitos = list(
        vaga.vagahabilidadetecnica_set.values_list("habilidade__nome", flat=True)
    )

    # ---------------------------
    # 1. Buscar usuários por skill
    # ---------------------------
    usuarios = github_buscar_usuarios(requisitos)

    if not usuarios:
        print("Nenhum perfil encontrado no GitHub.")
        return

    # ---------------------------
    # 2. Para cada usuário: detalhes + salvar
    # ---------------------------
    for u in usuarios:
        detalhes = github_detalhar_usuario(u["login"])
        if not detalhes:
            continue

        salvar_candidato_github(vaga, detalhes, requisitos)
