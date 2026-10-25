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


def gerar_novo_id(usuarios):
    """Devolve o próximo ID disponível (maior ID existente + 1)."""
    if not usuarios:
        return 1
    return max(usuario["id"] for usuario in usuarios) + 1


def cadastrar_usuario():
    """Pede os dados no terminal e cadastra um novo usuário."""
    usuarios = carregar_usuarios()

    print("\n--- Cadastrar usuário ---")
    nome = input("Nome: ").strip()
    if not nome:
        print("O nome não pode ficar vazio.")
        return

    email = input("E-mail: ").strip().lower()
    for usuario in usuarios:
        if usuario["email"] == email:
            print("Já existe um usuário com esse e-mail.")
            return

    print("Perfil: 1 - Professor | 2 - Coordenação")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        perfil = "professor"
    elif opcao == "2":
        perfil = "coordenacao"
    else:
        print("Opção inválida.")
        return

    turmas = []
    if perfil == "professor":
        texto = input("Turmas (separe por vírgula, ex: 6A_CIEN, 7B_CIEN): ")
        turmas = [t.strip().upper() for t in texto.split(",") if t.strip()]

    novo_usuario = {
        "id": gerar_novo_id(usuarios),
        "nome": nome,
        "email": email,
        "perfil": perfil,
        "turmas_lecionadas": turmas,
        "ativo": True,
    }
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    print(f"Usuário '{nome}' cadastrado com ID {novo_usuario['id']}.")


# Teste rápido: só roda quando executamos este arquivo diretamente
if __name__ == "__main__":
    cadastrar_usuario()
    for usuario in carregar_usuarios():
        print(usuario["id"], "-", usuario["nome"], "-", usuario["perfil"])