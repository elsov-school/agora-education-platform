import re
import unicodedata

from database import connect, transaction
from services.library import list_materials


STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e", "em",
    "para", "por", "que", "com", "na", "no", "nas", "nos", "se", "ao", "aos", "sua",
    "seu", "suas", "seus", "como", "mais", "menos", "tambem", "entre",
}


def _normalize(text):
    normalized = unicodedata.normalize("NFKD", text.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _tokens(text):
    return {
        word for word in re.findall(r"[a-z0-9]+", _normalize(text))
        if len(word) > 2 and word not in STOPWORDS
    }


def _sentences(text):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text.strip()) if len(part.split()) >= 4]


def verify_content(data, teacher, database_path=None):
    title = data.get("title", "").strip() or "Conteúdo para verificação"
    content = data.get("content", "").strip()
    class_name = data.get("class_name", "").strip()
    subject = data.get("subject", "").strip()
    if not content or not class_name or not subject:
        raise ValueError("Informe turma, disciplina e o conteúdo que será verificado.")
    if class_name not in teacher["classes"] or subject not in teacher["subjects"]:
        raise ValueError("A turma ou disciplina não pertence ao perfil do professor.")

    materials = list_materials(
        {"class_name": class_name, "subject": subject},
        user=teacher, approved_only=True, database_path=database_path,
    )
    selected_ids = {int(value) for value in data.getlist("material_ids")}
    if selected_ids:
        materials = [material for material in materials if material["id"] in selected_ids]
    if not materials:
        raise ValueError("Não há materiais aprovados selecionados para essa verificação.")

    evidence_pool = []
    for material in materials:
        for excerpt in _sentences(material["content"]):
            evidence_pool.append((excerpt, material, _tokens(excerpt)))

    claims = _sentences(content)
    if not claims:
        raise ValueError("O conteúdo precisa possuir ao menos uma afirmação completa.")

    items = []  # Lista de dicionários: cada afirmação e seu diagnóstico institucional.
    for position, claim in enumerate(claims, 1):
        claim_tokens = _tokens(claim)
        best = (0.0, None, None)
        for excerpt, material, evidence_tokens in evidence_pool:
            if not claim_tokens:
                continue
            score = len(claim_tokens & evidence_tokens) / len(claim_tokens)
            if score > best[0]:
                best = (score, excerpt, material)
        score, excerpt, material = best
        if score >= 0.55:
            status = "Suportado"
        elif score >= 0.25:
            status = "Parcialmente suportado"
        else:
            status, excerpt, material = "Nao localizado", None, None
        items.append({
            "claim": claim, "status": status, "matched_excerpt": excerpt,
            "material_id": material["id"] if material else None,
            "score": score, "position": position,
        })

    with transaction(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO verifications (title, content, class_name, subject, teacher_id) VALUES (?, ?, ?, ?, ?)",
            (title, content, class_name, subject, teacher["id"]),
        )
        verification_id = cursor.lastrowid
        connection.executemany(
            """INSERT INTO verification_items
            (verification_id, claim, status, matched_excerpt, material_id, score, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (verification_id, item["claim"], item["status"], item["matched_excerpt"],
                 item["material_id"], item["score"], item["position"])
                for item in items
            ],
        )
    return verification_id


def get_verification(verification_id, teacher_id=None, database_path=None):
    connection = connect(database_path)
    params = [verification_id]
    where = "v.id=?"
    if teacher_id:
        where += " AND v.teacher_id=?"
        params.append(teacher_id)
    row = connection.execute(
        f"""SELECT v.*, u.name AS teacher_name FROM verifications v
        JOIN users u ON u.id=v.teacher_id WHERE {where}""", params
    ).fetchone()
    if not row:
        connection.close()
        return None
    verification = dict(row)
    items = connection.execute(
        """SELECT vi.*, m.title AS material_title, m.bncc, m.author_source
        FROM verification_items vi LEFT JOIN materials m ON m.id=vi.material_id
        WHERE vi.verification_id=? ORDER BY vi.position""",
        (verification_id,),
    ).fetchall()
    verification["items"] = [dict(item) for item in items]
    verification["counts"] = {
        "supported": sum(item["status"] == "Suportado" for item in verification["items"]),
        "partial": sum(item["status"] == "Parcialmente suportado" for item in verification["items"]),
        "not_found": sum(item["status"] == "Nao localizado" for item in verification["items"]),
    }
    connection.close()
    return verification


def list_verifications(teacher_id, database_path=None):
    connection = connect(database_path)
    rows = connection.execute(
        """SELECT v.*, COUNT(vi.id) AS item_count,
        SUM(CASE WHEN vi.status='Nao localizado' THEN 1 ELSE 0 END) AS not_found
        FROM verifications v LEFT JOIN verification_items vi ON vi.verification_id=v.id
        WHERE v.teacher_id=? GROUP BY v.id ORDER BY v.created_at DESC""",
        (teacher_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]
