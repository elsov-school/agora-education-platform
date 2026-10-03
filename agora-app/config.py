from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "agora.db"
SECRET_KEY = "agora-prototipo-academico"

# Tupla: conjunto fixo e imutavel de tipos aceitos pelo gerador.
TIPOS_QUESTAO = (
    "Multipla escolha",
    "Discursiva",
    "Verdadeiro ou falso",
)

DIFICULDADES = ("Facil", "Media", "Dificil")
STATUS_CONTEUDO = ("Rascunho", "Pendente de validacao", "Aprovado", "Reprovado")

