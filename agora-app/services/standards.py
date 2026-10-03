import json

from config import DIFICULDADES, TIPOS_QUESTAO
from database import connect, transaction


def get_settings(database_path=None):
    connection = connect(database_path)
    row = connection.execute("SELECT * FROM settings WHERE id = 1").fetchone()
    connection.close()
    settings = dict(row)
    settings["allowed_types"] = json.loads(settings["allowed_types"])
    settings["require_source"] = bool(settings["require_source"])
    return settings


def update_settings(data, database_path=None):
    max_questions = max(1, min(50, int(data["max_questions"])))
    allowed = [kind for kind in data.getlist("allowed_types") if kind in TIPOS_QUESTAO]
    if not allowed:
        raise ValueError("Selecione ao menos um tipo de questao.")
    difficulty = data["default_difficulty"]
    if difficulty not in DIFICULDADES:
        raise ValueError("Dificuldade invalida.")
    with transaction(database_path) as connection:
        connection.execute(
            """UPDATE settings SET max_questions=?, allowed_types=?, default_difficulty=?,
            require_source=?, header_template=?, quality_criteria=?, approval_rules=?, instructions=? WHERE id=1""",
            (
                max_questions, json.dumps(allowed), difficulty, 1 if data.get("require_source") else 0,
                data["header_template"].strip(), data["quality_criteria"].strip(),
                data["approval_rules"].strip(), data["instructions"].strip(),
            ),
        )
