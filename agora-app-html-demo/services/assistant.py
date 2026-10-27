import re
import unicodedata

from services.library import list_materials


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e",
    "em", "para", "por", "qual", "quais", "que", "como", "com", "na", "no", "nas",
    "nos", "sua", "seu", "sobre", "segundo", "material", "funcao", "eh", "e",
}


def _normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def _tokens(text):
    return {word for word in re.findall(r"[a-z0-9]+", _normalize(text)) if len(word) > 2 and word not in STOPWORDS}


def answer_question(question, class_name, subject, user, database_path=None):
    query_tokens = _tokens(question)
    if not query_tokens:
        return {"answer": None, "evidence": []}
    materials = list_materials(
        {"class_name": class_name, "subject": subject}, user=user, approved_only=True, database_path=database_path
    )
    candidates = []  # Lista de tuplas: (pontuacao, trecho, material).
    for material in materials:
        for sentence in re.split(r"(?<=[.!?])\s+", material["content"]):
            overlap = query_tokens & _tokens(sentence)
            if overlap:
                score = len(overlap) / max(1, len(query_tokens))
                candidates.append((score, sentence.strip(), material))
    candidates.sort(key=lambda item: item[0], reverse=True)
    if not candidates or candidates[0][0] < 0.20:
        return {"answer": None, "evidence": []}
    selected = candidates[:2]
    evidence = [
        {"material_id": material["id"], "title": material["title"], "bncc": material["bncc"], "excerpt": sentence}
        for _, sentence, material in selected
    ]
    return {"answer": " ".join(item["excerpt"] for item in evidence), "evidence": evidence}

