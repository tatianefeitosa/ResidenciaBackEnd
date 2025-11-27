'''
import requests
from bs4 import BeautifulSoup
import re
import time

BASE_URL = "https://github.com"

def normalize_text(text):
    if not text:
        return ""
    return text.strip().lower()

def extract_emails(text):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

def extract_phones(text):
    return re.findall(r"\+?\d[\d\s()-]{7,}\d", text)

def scrape_profile(url, requisitos):
    """
    Scrape um perfil do GitHub e calcula compatibilidade baseada nos requisitos.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Nome e bio
    nome_tag = soup.select_one("span.p-name.vcard-fullname")
    nome = nome_tag.get_text(strip=True) if nome_tag else "Sem Nome"

    bio_tag = soup.select_one("div.p-note")
    resumo_profissional = bio_tag.get_text(strip=True) if bio_tag else ""

    # Localização
    loc_tag = soup.select_one("li[itemprop='homeLocation']")
    localizacao = loc_tag.get_text(strip=True) if loc_tag else ""

    # Empresas
    empresa_tag = soup.select_one("li[itemprop='worksFor']")
    empresas = [empresa_tag.get_text(strip=True)] if empresa_tag else []

    # URLs e fonte
    fonte_busca = BASE_URL
    url_perfil = url

    # Extração simples de skills, idiomas, diplomas, certificações (tentativa via bio e readme)
    habilidades_tecnicas = []
    habilidades_interpessoais = []
    diplomas = []
    certificacoes = []
    idiomas = []

    # Pegando readme do usuário (se existir)
    readme_url = f"{url}.atom"  # feed público do usuário
    try:
        readme_resp = requests.get(readme_url, headers=headers)
        if readme_resp.ok:
            readme_text = readme_resp.text
        else:
            readme_text = ""
    except:
        readme_text = ""

    combined_text = " ".join([resumo_profissional, readme_text, localizacao, " ".join(empresas)])

    # Emails e telefones
    emails = extract_emails(combined_text)
    telefones = extract_phones(combined_text)

    # Compatibilidade simples
    compatibilidade = 0
    for req in requisitos:
        req_norm = normalize_text(req)
        if req_norm in normalize_text(combined_text):
            compatibilidade += 1

    candidato = {
        "nome": nome,
        "resumo_profissional": resumo_profissional,
        "habilidades_tecnicas": habilidades_tecnicas,
        "habilidades_interpessoais": habilidades_interpessoais,
        "diplomas": diplomas,
        "certificacoes": certificacoes,
        "idiomas": idiomas,
        "empresas": empresas,
        "localizacoes": [localizacao] if localizacao else [],
        "emails": emails,
        "telefones": telefones,
        "fonte_nome": "GitHub",
        "url_perfil": url_perfil,
        "similarity_score": compatibilidade / max(len(requisitos), 1),
        "raw_result": combined_text,
        "source_id": url_perfil,
    }

    return candidato

def scrape_top_candidatos(vaga, requisitos, top_n=5):
    """
    Faz scraping simples no GitHub por cada requisito da vaga.
    Retorna os top_n candidatos mais compatíveis.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    candidatos = []
    seen_profiles = set()

    for req in requisitos:
        search_url = f"{BASE_URL}/search?q={req}&type=users"
        resp = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        profile_links = soup.select("div.user-list div.d-flex a[href^='/']")  # links de perfis

        for link in profile_links:
            profile_url = BASE_URL + link["href"]
            if profile_url in seen_profiles:
                continue
            try:
                candidato = scrape_profile(profile_url, requisitos)
                candidatos.append(candidato)
                seen_profiles.add(profile_url)
            except Exception as e:
                print(f"[ERROR] Não foi possível extrair perfil {profile_url}: {e}")
            if len(candidatos) >= top_n:
                break
        if len(candidatos) >= top_n:
            break
        time.sleep(1)  # evitar bloqueio GitHub

    # Ordena por compatibilidade
    candidatos = sorted(candidatos, key=lambda x: x["similarity_score"], reverse=True)
    return candidatos[:top_n]
