import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.utils import timezone
from candidatos.models import Candidato

GITHUB_API = "https://api.github.com"
TIMEOUT = 10


def github_request(url, params=None):
    """
    Wrapper inteligente para evitar bloqueios, limites e adicionar timeout.
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "BuscaCandidatoScraper"
    }

    response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)

    if response.status_code == 403:
        raise Exception("Limite da API do GitHub atingido.")
    if response.status_code not in (200, 201):
        raise Exception(f"Erro GitHub API ({response.status_code}): {response.text}")

    return response.json()


def search_github_users(query, limit=20):
    """
    Procura usuários no GitHub com base nos requisitos da vaga.
    """
    url = f"{GITHUB_API}/search/users"
    params = {"q": query, "per_page": limit}

    data = github_request(url, params=params)

    return data.get("items", [])


def get_user_details(username):
    """
    Coleta informações detalhadas do usuário.
    """
    user = github_request(f"{GITHUB_API}/users/{username}")

    repos = github_request(f"{GITHUB_API}/users/{username}/repos")

    repo_info = []
    languages = []

    for r in repos:
        repo_info.append({
            "name": r["name"],
            "description": r["description"],
            "topics": r.get("topics", []),
            "language": r.get("language")
        })
        if r.get("language"):
            languages.append(r["language"])

    df_repos = pd.DataFrame(repo_info)

    return {
        "user": user,
        "repos": df_repos.to_dict(orient="records"),
        "languages": languages
    }


def compute_match_score(requisitos_texto, dados):
    """
    Gera um score simples (pode evoluir para TF-IDF ou ML futuramente).
    """
    texto = (
        (dados["user"].get("bio") or "") +
        " ".join(dados["languages"])
    ).lower()

    score = 0
    for req in requisitos_texto:
        if req.lower() in texto:
            score += 1

    return score


def generate_source_hash(username):
    """
    Garante idempotência: candidatos não são duplicados.
    """
    return hashlib.sha256(f"github:{username}".encode()).hexdigest()


def save_candidate_from_github(vaga, detalhes, score):
    """
    Salva/atualiza candidato no banco através do modelo Candidato.
    """
    username = detalhes["user"]["login"]
    hash_id = generate_source_hash(username)

    candidato, created = Candidato.objects.update_or_create(
        source_id_hash=hash_id,
        defaults={
            "vaga": vaga,
            "nome_candidato": detalhes["user"].get("name") or username,
            "email_contato": detalhes["user"].get("email"),
            "origem": "GitHub",
            "score_afinidade": score,
            "raw_result": detalhes,
            "data_atualizacao": timezone.now()
        }
    )

    return candidato


def run_github_scraping(vaga, requisitos_texto):
    """
    Função principal chamada pela task Celery.
    """
    print(f"[GitHub Scraper] Iniciando scraping para a vaga {vaga.id}...")

    # 1. Construir query de busca
    query = " ".join(requisitos_texto)

    usuarios = search_github_users(query)

    candidatos_criados = []

    for u in usuarios:
        username = u["login"]

        try:
            detalhes = get_user_details(username)

            score = compute_match_score(requisitos_texto, detalhes)

            candidato = save_candidate_from_github(vaga, detalhes, score)

            candidatos_criados.append(candidato)

        except Exception as e:
            print(f"Erro ao processar {username}: {str(e)}")

    print(f"[GitHub Scraper] Finalizado. {len(candidatos_criados)} candidatos coletados.")

    return candidatos_criados
