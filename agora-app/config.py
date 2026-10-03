import os
from pathlib import Path
from tempfile import gettempdir


BASE_DIR = Path(__file__).resolve().parent
DEMO_MODE = os.environ.get("VERCEL") == "1"
DEFAULT_DATABASE_PATH = (
    Path(gettempdir()) / "agora-demo" / "agora.db"
    if DEMO_MODE else BASE_DIR / "data" / "agora.db"
)
DATABASE_PATH = Path(os.environ.get("DATABASE_PATH") or DEFAULT_DATABASE_PATH)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEMO_MODE:
        raise RuntimeError("Configure SECRET_KEY no projeto da Vercel antes de publicar.")
    SECRET_KEY = "agora-prototipo-academico"

# Tupla: conjunto fixo e imutavel de tipos aceitos pelo gerador.
TIPOS_QUESTAO = (
    "Multipla escolha",
    "Discursiva",
    "Verdadeiro ou falso",
)

DIFICULDADES = ("Facil", "Media", "Dificil")
STATUS_CONTEUDO = ("Rascunho", "Pendente de validacao", "Aprovado", "Reprovado")
