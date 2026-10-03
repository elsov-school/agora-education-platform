import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from config import DATABASE_PATH


def connect(database_path=None):
    path = database_path or DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def transaction(database_path=None):
    connection = connect(database_path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Professor', 'Coordenacao')),
    subjects TEXT NOT NULL DEFAULT '[]',
    classes TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    material_type TEXT NOT NULL,
    school_year INTEGER NOT NULL,
    class_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    bimester INTEGER NOT NULL,
    bncc TEXT NOT NULL,
    author_source TEXT NOT NULL,
    content TEXT NOT NULL,
    approval_status TEXT NOT NULL DEFAULT 'Pendente'
        CHECK(approval_status IN ('Aprovado', 'Pendente', 'Reprovado')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    max_questions INTEGER NOT NULL DEFAULT 10,
    allowed_types TEXT NOT NULL,
    default_difficulty TEXT NOT NULL DEFAULT 'Media',
    require_source INTEGER NOT NULL DEFAULT 1,
    header_template TEXT NOT NULL,
    quality_criteria TEXT NOT NULL,
    approval_rules TEXT NOT NULL,
    instructions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    class_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    teacher_id INTEGER NOT NULL REFERENCES users(id),
    status TEXT NOT NULL DEFAULT 'Rascunho',
    reviewer_id INTEGER REFERENCES users(id),
    reviewed_at TEXT,
    review_note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    question_type TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    answer TEXT NOT NULL,
    source_material_id INTEGER REFERENCES materials(id),
    position INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS material_usage (
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    PRIMARY KEY(material_id, activity_id)
);

CREATE TABLE IF NOT EXISTS verifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    class_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    teacher_id INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS verification_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verification_id INTEGER NOT NULL REFERENCES verifications(id) ON DELETE CASCADE,
    claim TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Suportado', 'Parcialmente suportado', 'Nao localizado')),
    matched_excerpt TEXT,
    material_id INTEGER REFERENCES materials(id),
    score REAL NOT NULL DEFAULT 0,
    position INTEGER NOT NULL
);
"""


def init_database(database_path=None):
    with transaction(database_path) as connection:
        connection.executescript(SCHEMA)
        seed_database(connection)


def seed_database(connection):
    if connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
        return

    # Lista de dicionarios: estrutura central para os registros iniciais.
    users = [
        {"id": 1, "name": "Ana Souza", "role": "Professor", "subjects": ["Ciencias", "Biologia"], "classes": ["8o ano A", "1o ano EM"]},
        {"id": 2, "name": "Carlos Lima", "role": "Professor", "subjects": ["Matematica"], "classes": ["8o ano A", "9o ano B"]},
        {"id": 3, "name": "Marina Costa", "role": "Professor", "subjects": ["Portugues"], "classes": ["8o ano A"]},
        {"id": 4, "name": "Paula Mendes", "role": "Coordenacao", "subjects": [], "classes": []},
    ]
    connection.executemany(
        "INSERT INTO users (id, name, role, subjects, classes) VALUES (:id, :name, :role, :subjects, :classes)",
        [{**user, "subjects": json.dumps(user["subjects"]), "classes": json.dumps(user["classes"])} for user in users],
    )

    materials = [
        ("Citologia: organelas celulares", "Apostila", 2026, "1o ano EM", "Biologia", 1, "EM13CNT202", "Equipe de Ciencias", "A mitocondria participa da respiracao celular e da producao de energia na forma de ATP. O nucleo armazena o material genetico e coordena as atividades celulares. Os ribossomos realizam a sintese de proteinas.", "Aprovado"),
        ("Ecossistemas e cadeias alimentares", "Texto didatico", 2026, "8o ano A", "Ciencias", 2, "EF07CI07", "Secretaria Pedagogica", "Em uma cadeia alimentar, os produtores fabricam seu proprio alimento por fotossintese. Os consumidores obtem energia ao se alimentar de outros seres vivos. Os decompositores reciclam a materia organica no ambiente.", "Aprovado"),
        ("Proporcionalidade e porcentagem", "Caderno de exercicios", 2026, "8o ano A", "Matematica", 1, "EF08MA04", "Prof. Carlos Lima", "Porcentagem representa uma razao de denominador cem. Para calcular 20 por cento de 150, multiplicamos 150 por 0,20 e obtemos 30. Grandezas diretamente proporcionais variam na mesma razao.", "Aprovado"),
        ("Equacoes do segundo grau", "Apostila", 2026, "9o ano B", "Matematica", 2, "EF09MA09", "Equipe de Matematica", "Uma equacao do segundo grau tem a forma ax ao quadrado mais bx mais c igual a zero, com a diferente de zero. O discriminante delta e calculado por b ao quadrado menos quatro vezes a vezes c.", "Aprovado"),
        ("Generos argumentativos", "Sequencia didatica", 2026, "8o ano A", "Portugues", 1, "EF89LP10", "Profa. Marina Costa", "O artigo de opiniao apresenta uma tese sobre um tema relevante. Os argumentos sustentam a tese com dados, exemplos e relacoes logicas. A conclusao retoma a ideia principal do texto.", "Aprovado"),
        ("Genetica introdutoria", "Resumo", 2026, "1o ano EM", "Biologia", 2, "EM13CNT205", "Equipe de Ciencias", "O DNA contem informacoes hereditarias organizadas em genes. Os cromossomos sao estruturas formadas por DNA associado a proteinas.", "Pendente"),
    ]
    connection.executemany(
        """INSERT INTO materials
        (title, material_type, school_year, class_name, subject, bimester, bncc, author_source, content, approval_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        materials,
    )

    connection.execute(
        """INSERT INTO settings
        (id, max_questions, allowed_types, default_difficulty, require_source, header_template, quality_criteria, approval_rules, instructions)
        VALUES (1, 10, ?, 'Media', 1, ?, ?, ?, ?)""",
        (
            json.dumps(["Multipla escolha", "Discursiva", "Verdadeiro ou falso"]),
            "Escola Agora | Avaliacao institucional | Nome: __________ Turma: _____",
            "Clareza, alinhamento a BNCC e uso de evidencias institucionais.",
            "Toda atividade deve possuir fontes aprovadas e gabarito verificavel.",
            "Use linguagem adequada a serie e evite informacoes externas aos materiais.",
        ),
    )

    now = datetime.now().isoformat(timespec="minutes")
    activities = [
        ("Atividade de Citologia", "1o ano EM", "Biologia", 1, "Pendente de validacao", None, None, None),
        ("Revisao de Porcentagem", "8o ano A", "Matematica", 2, "Aprovado", 4, now, "Conteudo claro e alinhado ao material institucional."),
    ]
    connection.executemany(
        """INSERT INTO activities
        (title, class_name, subject, teacher_id, status, reviewer_id, reviewed_at, review_note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        activities,
    )
    connection.executemany(
        """INSERT INTO questions
        (activity_id, prompt, question_type, difficulty, answer, source_material_id, position)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            (1, "Qual e a principal funcao da mitocondria segundo o material?", "Discursiva", "Media", "Participar da respiracao celular e produzir energia na forma de ATP.", 1, 1),
            (2, "Quanto e 20 por cento de 150?", "Discursiva", "Facil", "30.", 3, 1),
        ],
    )
    connection.executemany(
        "INSERT INTO material_usage (material_id, activity_id) VALUES (?, ?)",
        [(1, 1), (3, 2)],
    )


def row_to_dict(row):
    return dict(row) if row else None
