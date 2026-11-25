"""Entrada do protótipo Ágora. Execute com py main.py."""

from consultas import consultas
from materiais import materiais
from padroes import padroes
from painel.painel import menu_painel
from provas import provas
from usuarios import usuarios


def usuario_da_sessao(usuario, perfil):
    """Relê o cadastro para reconhecer desativação e mudanças de atribuição."""
    if not usuario or not usuario.get("ativo") or usuario.get("perfil") != perfil:
        return None
    atual = usuarios.buscar_usuario(usuarios.carregar_usuarios(), usuario["id"])
    if atual and atual.get("ativo") and atual.get("perfil") == perfil:
        return atual
    return None


def menu_coordenacao(usuario):
    while True:
        usuario = usuario_da_sessao(usuario, "coordenacao")
        if not usuario:
            print("Acesso restrito à coordenação ativa.")
            return
        print(f"\nCOORDENAÇÃO | {usuario['nome']}")
        print("1 - Gerenciar usuários e atribuições")
        print("2 - Gerenciar biblioteca")
        print("3 - Aprovar materiais pendentes")
        print("4 - Configurar padrão da escola")
        print("5 - Painel de métricas")
        print("6 - Provas e histórico")
        print("9 - Trocar de usuário")
        print("0 - Sair do programa")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            usuarios.gerenciar_usuarios(usuario)
        elif opcao == "2":
            materiais.gerenciar_materiais(usuario)
        elif opcao == "3":
            materiais.aprovar_materiais_pendentes(usuario)
        elif opcao == "4":
            padroes.configurar_padrao_escola(usuario)
        elif opcao == "5":
            menu_painel(usuario)
        elif opcao == "6":
            provas.gerenciar_provas(usuario)
        elif opcao == "9":
            return
        elif opcao == "0":
            return "sair"
        else:
            print("Opção inválida.")


def menu_professor(usuario):
    while True:
        usuario = usuario_da_sessao(usuario, "professor")
        if not usuario:
            print("Acesso restrito a professores ativos.")
            return
        print(f"\nPROFESSOR | {usuario['nome']}")
        print("1 - Pesquisar na minha biblioteca")
        print("2 - Sugerir material")
        print("3 - Consultar conteúdo com evidência")
        print("4 - Gerar prova")
        print("5 - Gerenciar provas, histórico e exportação")
        print("9 - Trocar de usuário")
        print("0 - Sair do programa")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            consultas.pesquisar_material(usuario)
        elif opcao == "2":
            materiais.adicionar_material(usuario)
        elif opcao == "3":
            consultas.consultar_com_evidencia(usuario)
        elif opcao == "4":
            provas.gerar_prova(usuario)
        elif opcao == "5":
            provas.gerenciar_provas(usuario)
        elif opcao == "9":
            return
        elif opcao == "0":
            return "sair"
        else:
            print("Opção inválida.")


def menu_principal():
    print("\nÁGORA - BIBLIOTECA ESCOLAR")
    if not hasattr(usuarios, "fazer_login"):
        print("Para iniciar o login, integre a entrega contrato v1 do módulo usuários.")
        return
    if not materiais.carregar_dados():
        return
    while True:
        usuario = usuarios.fazer_login()
        if usuario is None:
            break
        if usuario.get("perfil") == "coordenacao":
            resultado = menu_coordenacao(usuario)
        elif usuario.get("perfil") == "professor":
            resultado = menu_professor(usuario)
        else:
            print("Perfil sem acesso ao sistema.")
            continue
        if resultado == "sair":
            break
    print("Até logo!")


if __name__ == "__main__":
    try:
        menu_principal()
    except (OSError, ValueError) as erro:
        print("Não foi possível acessar os dados da escola:", erro)
    except (EOFError, KeyboardInterrupt):
        print("\nSessão encerrada.")
