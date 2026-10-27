from datetime import datetime

from database import connect, transaction


def submit_activity(activity_id, teacher_id, database_path=None):
    with transaction(database_path) as connection:
        activity = connection.execute(
            "SELECT * FROM activities WHERE id=? AND teacher_id=?", (activity_id, teacher_id)
        ).fetchone()
        if not activity or activity["status"] not in ("Rascunho", "Reprovado"):
            raise ValueError("Esta atividade nao pode ser enviada neste estado.")
        question_count = connection.execute(
            "SELECT COUNT(*) FROM questions WHERE activity_id=?", (activity_id,)
        ).fetchone()[0]
        if question_count == 0:
            raise ValueError("Inclua ao menos uma questao antes do envio.")
        connection.execute(
            "UPDATE activities SET status='Pendente de validacao', reviewer_id=NULL, reviewed_at=NULL, review_note=NULL WHERE id=?",
            (activity_id,),
        )


def review_activity(activity_id, reviewer_id, decision, note, database_path=None):
    if decision not in ("Aprovado", "Reprovado"):
        raise ValueError("Decisao invalida.")
    if decision == "Reprovado" and not note.strip():
        raise ValueError("Informe uma justificativa para reprovar.")
    with transaction(database_path) as connection:
        current = connection.execute("SELECT status FROM activities WHERE id=?", (activity_id,)).fetchone()
        if not current or current["status"] != "Pendente de validacao":
            raise ValueError("Somente conteudos pendentes podem ser analisados.")
        connection.execute(
            "UPDATE activities SET status=?, reviewer_id=?, reviewed_at=?, review_note=? WHERE id=?",
            (decision, reviewer_id, datetime.now().isoformat(timespec="minutes"), note.strip(), activity_id),
        )


def pending_activities(database_path=None):
    connection = connect(database_path)
    rows = connection.execute(
        """SELECT a.*, u.name AS teacher_name, COUNT(q.id) AS question_count
        FROM activities a JOIN users u ON u.id=a.teacher_id
        LEFT JOIN questions q ON q.activity_id=a.id
        WHERE a.status='Pendente de validacao'
        GROUP BY a.id ORDER BY a.created_at"""
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]
