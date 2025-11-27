'''candidatos/nlp_matcher.py
import os
import logging
import spacy
from functools import lru_cache

logger = logging.getLogger(__name__)
# carrega modelo grande em PT
# certifique-se de ter feito: python -m spacy download pt_core_news_lg
@lru_cache(maxsize=1)
def get_nlp():
    return spacy.load("pt_core_news_lg")

def build_requisitos_docs(requisitos_by_category):
    """
    requisitos_by_category: dict: category -> list[str]
    retorna dict category -> list of (string, doc)
    """
    nlp = get_nlp()
    docs = {}
    for cat, items in requisitos_by_category.items():
        docs[cat] = [(it, nlp(it)) for it in (items or [])]
    return docs

def candidate_text_from_payload(payload):
    """
    Junta bio + repo descriptions + repo topics + company + location
    Retorna plain text concatenado (string)
    """
    parts = []
    bio = payload.get("bio") or ""
    parts.append(bio)
    if payload.get("company"):
        parts.append(str(payload.get("company")))
    if payload.get("location"):
        parts.append(str(payload.get("location")))
    # repos
    for r in payload.get("repos", []):
        if r.get("description"):
            parts.append(r.get("description"))
        if r.get("topics"):
            parts.extend([t for t in r.get("topics") if t])
        if r.get("language"):
            parts.append(r.get("language"))
    text = " . ".join([p for p in parts if p])
    return text

def match_candidate_to_requisitos(payload, requisitos_by_category, thresholds=None):
    """
    payload: candidate payload from github_scraper
    requisitos_by_category: dict like { 'certificacoes': ['Amazon Web Services', ...], ... }
    thresholds: dict category -> float (similarity threshold). Default 0.72.
    Retorna: mapping category -> list of matched requisito strings (empty if none), and a compatibility score 0-100
    """
    if thresholds is None:
        thresholds = {}
    default_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.72"))

    nlp = get_nlp()
    requisitos_docs = build_requisitos_docs(requisitos_by_category)
    candidate_text = candidate_text_from_payload(payload)
    if not candidate_text.strip():
        return {"matches": {}, "compatibilidade": 0.0}

    cand_doc = nlp(candidate_text)

    matches = {}
    total_reqs = 0
    matched_count = 0

    for cat, items in requisitos_docs.items():
        matches[cat] = []
        for (req_str, req_doc) in items:
            total_reqs += 1
            # compute similarity between the requisito and the whole candidate text
            score = req_doc.similarity(cand_doc)
            threshold = thresholds.get(cat, default_threshold)
            if score >= threshold:
                matches[cat].append({"requisito": req_str, "score": float(score)})
                matched_count += 1

    compat = (matched_count / total_reqs * 100.0) if total_reqs > 0 else 0.0
    return {"matches": matches, "compatibilidade": round(compat, 2)}