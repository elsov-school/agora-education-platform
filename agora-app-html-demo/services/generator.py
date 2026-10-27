import json
import re

from config import DIFICULDADES, TIPOS_QUESTAO
from database import connect, transaction
from services.standards import get_settings


def _sentences(text):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if len(part.split()) >= 5]


def _question_from_sentence(sentence, material, question_type, difficulty, index, alternatives):
    source_label = material["title"]
    if question_type == "Discursiva":
        prompt = f"Explique, com base no material '{source_label}', a seguinte ideia: {sentence.split('.')[0]}."
        answer = sentence
    elif question_type == "Verdadeiro ou falso":
        prompt = f"Verdadeiro ou falso: {sentence}"
        answer = "Verdadeiro. A afirmacao corresponde ao material institucional selecionado."
    else:
        distractors = [item for item in alternatives if item != sentence][:3]
        while len(distractors) < 3:
            distractors.append("A afirmacao nao e apresentada nos materiais selecionados.")
        options = [sentence] + distractors
        # Rotacao deterministica evita que a resposta correta esteja sempre na alternativa A.
        shift = index % len(options)
        options = options[shift:] + options[:shift]
        letters = "ABCD"
        formatted = "\n".join(f"{letters[pos]}) {value}" for pos, value in enumerate(options))
        correct = letters[options.index(sentence)]
        prompt = f"Segundo '{source_label}', assinale a alternativa correta:\n{formatted}"
        answer = f"Alternativa {correct}: {sentence}"
    return {
        "prompt": prompt,
        "question_type": question_type,
        "difficulty": difficulty,
        "answer": answer,
        "source_material_id": material["id"],
    }


def generate_activity(data, teacher_id, database_path=None):
    settings = get_settings(database_path)
    quantity = int(data["quantity"])
    if quantity < 1 or quantity > settings["max_questions"]:
        raise ValueError(f"A quantidade deve estar entre 1 e {settings['max_questions']}.")
    question_type = data["question_type"]
    if question_type not in TIPOS_QUESTAO or question_type not in settings["allowed_types"]:
        raise ValueError("O tipo de questao nao e permitido pelo padrao institucional.")
    difficulty = data.get("difficulty") or settings["default_difficulty"]
    if difficulty not in DIFICULDADES:
        raise ValueError("Dificuldade invalida.")
    material_ids = [int(value) for value in data.getlist("material_ids")]
    if not material_ids:
        raise ValueError("Selecione ao menos um material institucional.")

    connection = connect(database_path)
    teacher = connection.execute("SELECT role, subjects, classes FROM users WHERE id=?", (teacher_id,)).fetchone()
    if not teacher or teacher["role"] != "Professor":
        connection.close()
        raise ValueError("Perfil de professor invalido.")
    if data["subject"] not in json.loads(teacher["subjects"]) or data["class_name"] not in json.loads(teacher["classes"]):
        connection.close()
        raise ValueError("A turma ou disciplina nao pertence ao perfil do professor.")
    placeholders = ",".join("?" for _ in material_ids)
    materials = connection.execute(
        f"SELECT * FROM materials WHERE id IN ({placeholders}) AND approval_status='Aprovado' AND class_name=? AND subject=?",
        [*material_ids, data["class_name"], data["subject"]],
    ).fetchall()
    connection.close()
    if len(materials) != len(set(material_ids)):
        raise ValueError("Use somente materiais aprovados da turma e disciplina selecionadas.")

    sentence_pool = []
    for material in materials:
        sentence_pool.extend((sentence, dict(material)) for sentence in _sentences(material["content"]))
    if not sentence_pool:
        raise ValueError("Os materiais selecionados nao possuem conteudo suficiente para gerar questoes.")
    alternatives = [sentence for sentence, _ in sentence_pool]
    questions = []  # Lista: colecao ordenada de questoes produzidas.
    for index in range(quantity):
        sentence, material = sentence_pool[index % len(sentence_pool)]
        questions.append(_question_from_sentence(sentence, material, question_type, difficulty, index, alternatives))

    title = data.get("title", "").strip() or f"Atividade de {data['subject']}"
    with transaction(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO activities (title, class_name, subject, teacher_id, status) VALUES (?, ?, ?, ?, 'Rascunho')",
            (title, data["class_name"], data["subject"], teacher_id),
        )
        activity_id = cursor.lastrowid
        connection.executemany(
            """INSERT INTO questions
            (activity_id, prompt, question_type, difficulty, answer, source_material_id, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (activity_id, question["prompt"], question["question_type"], question["difficulty"],
                 question["answer"], question["source_material_id"], position)
                for position, question in enumerate(questions, 1)
            ],
        )
        connection.executemany(
            "INSERT INTO material_usage (material_id, activity_id) VALUES (?, ?)",
            [(material_id, activity_id) for material_id in sorted(set(material_ids))],
        )
    return activity_id


def get_activity(activity_id, database_path=None):
    connection = connect(database_path)
    row = connection.execute(
        """SELECT a.*, teacher.name AS teacher_name, reviewer.name AS reviewer_name
        FROM activities a JOIN users teacher ON teacher.id=a.teacher_id
        LEFT JOIN users reviewer ON reviewer.id=a.reviewer_id WHERE a.id=?""",
        (activity_id,),
    ).fetchone()
    if not row:
        connection.close()
        return None
    activity = dict(row)
    questions = connection.execute(
        """SELECT q.*, m.title AS source_title, m.bncc AS source_bncc
        FROM questions q LEFT JOIN materials m ON m.id=q.source_material_id
        WHERE q.activity_id=? ORDER BY q.position, q.id""",
        (activity_id,),
    ).fetchall()
    activity["questions"] = [dict(question) for question in questions]
    sources = {}
    for question in activity["questions"]:
        if question["source_material_id"]:
            sources[question["source_material_id"]] = {
                "id": question["source_material_id"],
                "title": question["source_title"],
                "bncc": question["source_bncc"],
            }
    activity["sources"] = list(sources.values())
    activity["evidence_counts"] = {
        "supported": len(activity["questions"]),
        "partial": 0,
        "not_found": 0,
    }
    connection.close()
    return activity


def update_question(question_id, data, teacher_id, database_path=None):
    with transaction(database_path) as connection:
        question = connection.execute(
            """SELECT q.id FROM questions q JOIN activities a ON a.id=q.activity_id
            WHERE q.id=? AND a.teacher_id=? AND a.status IN ('Rascunho','Reprovado')""",
            (question_id, teacher_id),
        ).fetchone()
        if not question:
            raise ValueError("A questao nao pode ser editada.")
        connection.execute(
            "UPDATE questions SET prompt=?, answer=? WHERE id=?",
            (data["prompt"].strip(), data["answer"].strip(), question_id),
        )


def delete_question(question_id, teacher_id, database_path=None):
    with transaction(database_path) as connection:
        connection.execute(
            """DELETE FROM questions WHERE id=? AND activity_id IN
            (SELECT id FROM activities WHERE teacher_id=? AND status IN ('Rascunho','Reprovado'))""",
            (question_id, teacher_id),
        )


def regenerate_question(question_id, teacher_id, database_path=None):
    with transaction(database_path) as connection:
        row = connection.execute(
            """SELECT q.*, a.subject, a.class_name, m.content, m.title AS source_title
            FROM questions q JOIN activities a ON a.id=q.activity_id
            JOIN materials m ON m.id=q.source_material_id
            WHERE q.id=? AND a.teacher_id=? AND a.status IN ('Rascunho','Reprovado')""",
            (question_id, teacher_id),
        ).fetchone()
        if not row:
            raise ValueError("A questao nao pode ser trocada.")
        sentences = _sentences(row["content"])
        if not sentences:
            raise ValueError("A fonte nao possui outro trecho utilizavel.")
        current_index = next((i for i, sentence in enumerate(sentences) if sentence in row["answer"]), -1)
        sentence = sentences[(current_index + 1) % len(sentences)]
        material = {"id": row["source_material_id"], "title": row["source_title"]}
        generated = _question_from_sentence(sentence, material, row["question_type"], row["difficulty"], row["position"] + 1, sentences)
        connection.execute(
            "UPDATE questions SET prompt=?, answer=? WHERE id=?",
            (generated["prompt"], generated["answer"], question_id),
        )


def list_teacher_activities(teacher_id, database_path=None):
    connection = connect(database_path)
    rows = connection.execute(
        """SELECT a.*, COUNT(q.id) AS question_count FROM activities a
        LEFT JOIN questions q ON q.activity_id=a.id WHERE a.teacher_id=?
        GROUP BY a.id ORDER BY a.created_at DESC""",
        (teacher_id,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]
