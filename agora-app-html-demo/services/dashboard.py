from database import connect


def get_dashboard(database_path=None):
    connection = connect(database_path)
    counts = {
        "materials_total": connection.execute("SELECT COUNT(*) FROM materials").fetchone()[0],
        "materials_approved": connection.execute("SELECT COUNT(*) FROM materials WHERE approval_status='Aprovado'").fetchone()[0],
        "pending": connection.execute("SELECT COUNT(*) FROM activities WHERE status='Pendente de validacao'").fetchone()[0],
        "activities": connection.execute("SELECT COUNT(*) FROM activities").fetchone()[0],
    }
    by_subject = [dict(row) for row in connection.execute(
        "SELECT subject AS label, COUNT(*) AS value FROM materials GROUP BY subject ORDER BY value DESC"
    ).fetchall()]
    by_class = [dict(row) for row in connection.execute(
        "SELECT class_name AS label, COUNT(*) AS value FROM materials GROUP BY class_name ORDER BY value DESC"
    ).fetchall()]
    most_used = [dict(row) for row in connection.execute(
        """SELECT m.title, COUNT(mu.activity_id) AS uses FROM materials m
        LEFT JOIN material_usage mu ON mu.material_id=m.id GROUP BY m.id ORDER BY uses DESC, m.title LIMIT 5"""
    ).fetchall()]
    by_teacher = [dict(row) for row in connection.execute(
        """SELECT u.name, COUNT(a.id) AS total FROM users u
        LEFT JOIN activities a ON a.teacher_id=u.id WHERE u.role='Professor'
        GROUP BY u.id ORDER BY total DESC, u.name"""
    ).fetchall()]
    recent = [dict(row) for row in connection.execute(
        """SELECT a.id, a.title, a.status, a.subject, u.name AS teacher_name
        FROM activities a JOIN users u ON u.id=a.teacher_id ORDER BY a.created_at DESC LIMIT 6"""
    ).fetchall()]
    connection.close()
    max_subject = max((item["value"] for item in by_subject), default=1)
    for item in by_subject:
        item["percent"] = round(item["value"] / max_subject * 100)
    return {"counts": counts, "by_subject": by_subject, "by_class": by_class,
            "most_used": most_used, "by_teacher": by_teacher, "recent": recent}
