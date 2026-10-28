"""Usuários e perfis (Integrante 1). Contratos das funções em usuarios/README.md."""

import json
import os

# Caminho do JSON montado a partir da pasta deste arquivo,
# para funcionar de qualquer pasta em que o terminal esteja.
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_USUARIOS = os.path.join(PASTA_ATUAL, "usuarios.json")

# O que cada perfil pode fazer (usado por verificar_permissao).
PERMISSOES = {
    "coordenacao": {"gerenciar_usuarios", "aprovar_materiais", "acessar_metricas"},
    "professor": {"acessar_conteudos", "gerenciar_atividades"},
}


# ============================================================
# Funções de apoio (persistência e utilidades)
# ============================================================

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


def buscar_usuario(usuarios, usuario_id):
    """Procura um usuário pelo ID; devolve o dicionário ou None."""
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    return None


def normalizar_turmas(turmas_lecionadas):
    """Padroniza a lista de turmas: sem espaços, maiúsculas e sem itens vazios."""
    return [t.strip().upper() for t in turmas_lecionadas if t.strip()]


# ============================================================
# Funções do contrato (lógica, sem input/print)
# ============================================================

def cadastrar_professor(nome, email, turmas_lecionadas):
    """Valida nome e e-mail único, gera ID e salva um professor ativo."""
    nome = nome.strip()
    email = email.strip().lower()

    if not nome:
        raise ValueError("O nome não pode ficar vazio.")
    if "@" not in email:
        raise ValueError("Informe um e-mail válido.")

    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["email"] == email:
            raise ValueError("Já existe um usuário com esse e-mail.")

    novo_professor = {
        "id": gerar_novo_id(usuarios),
        "nome": nome,
        "email": email,
        "perfil": "professor",
        "turmas_lecionadas": normalizar_turmas(turmas_lecionadas),
        "ativo": True,
    }
    usuarios.append(novo_professor)
    salvar_usuarios(usuarios)
    return novo_professor


def listar_professores(incluir_inativos=False):
    """Devolve o corpo docente; omite inativos, a menos que se peça."""
    professores = []
    for usuario in carregar_usuarios():
        if usuario["perfil"] != "professor":
            continue
        if not usuario["ativo"] and not incluir_inativos:
            continue
        professores.append(usuario)
    return professores


def atualizar_turmas(usuario_id, turmas_lecionadas):
    """Substitui as turmas de um professor existente."""
    usuarios = carregar_usuarios()
    usuario = buscar_usuario(usuarios, usuario_id)

    if usuario is None:
        raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
    if usuario["perfil"] != "professor":
        raise ValueError("Só é possível atribuir turmas a professores.")

    usuario["turmas_lecionadas"] = normalizar_turmas(turmas_lecionadas)
    salvar_usuarios(usuarios)
    return usuario


def desativar_usuario(usuario_id):
    """Marca o usuário como inativo, sem apagá-lo (preserva o histórico)."""
    usuarios = carregar_usuarios()
    usuario = buscar_usuario(usuarios, usuario_id)

    if usuario is None:
        raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
    if not usuario["ativo"]:
        raise ValueError("Esse usuário já está inativo.")

    usuario["ativo"] = False
    salvar_usuarios(usuarios)
    return usuario


def verificar_permissao(usuario_id, acao):
    """Devolve True se o usuário existe, está ativo e o perfil permite a ação."""
    usuario = buscar_usuario(carregar_usuarios(), usuario_id)

    if usuario is None or not usuario["ativo"]:
        return False
    return acao in PERMISSOES.get(usuario["perfil"], set())


# ============================================================
# Interface no terminal (menu da coordenação)
# ============================================================

def ler_turmas():
    """Pede as turmas no terminal e devolve uma lista."""
    texto = input("Turmas (separe por vírgula, ex: 6A_CIEN, 7B_CIEN): ")
    return texto.split(",")


def mostrar_professores(professores):
    """Exibe uma lista de professores no terminal."""
    if not professores:
        print("Nenhum professor encontrado.")
        return
    for professor in professores:
        situacao = "Ativo" if professor["ativo"] else "Inativo"
        turmas = ", ".join(professor["turmas_lecionadas"]) or "-"
        print(f"[{professor['id']}] {professor['nome']} | {professor['email']} | "
              f"Turmas: {turmas} | {situacao}")


def gerenciar_usuarios():
    """Menu do CRUD de usuários, usado pela coordenação."""
    while True:
        print("\n=== Gestão de Usuários ===")
        print("1 - Cadastrar professor")
        print("2 - Listar professores ativos")
        print("3 - Listar todos (inclui inativos)")
        print("4 - Atualizar turmas de um professor")
        print("5 - Desativar usuário")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome: ")
                email = input("E-mail: ")
                professor = cadastrar_professor(nome, email, ler_turmas())
                print(f"Professor '{professor['nome']}' cadastrado com ID {professor['id']}.")
            elif opcao == "2":
                mostrar_professores(listar_professores())
            elif opcao == "3":
                mostrar_professores(listar_professores(incluir_inativos=True))
            elif opcao == "4":
                usuario_id = int(input("ID do professor: "))
                professor = atualizar_turmas(usuario_id, ler_turmas())
                print(f"Turmas de '{professor['nome']}' atualizadas.")
            elif opcao == "5":
                usuario_id = int(input("ID do usuário: "))
                usuario = desativar_usuario(usuario_id)
                print(f"Usuário '{usuario['nome']}' desativado.")
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
        except ValueError as erro:
            print(f"Erro: {erro}")


# Teste rápido: só roda quando executamos este arquivo diretamente
if __name__ == "__main__":
    gerenciar_usuarios()
