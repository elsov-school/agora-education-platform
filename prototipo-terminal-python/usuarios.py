import json

ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios():
    """Lê o arquivo JSON e devolve a lista de usuários."""
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar_usuarios(usuarios):
    """Grava a lista de usuários de volta no arquivo JSON."""
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)


# Teste rápido: só roda quando executamos este arquivo diretamente
if __name__ == "__main__":
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        print(usuario["id"], "-", usuario["nome"], "-", usuario["perfil"])