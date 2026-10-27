from materiais import carregar_dados, adicionar_material, gerenciar_materiais
from consultas import pesquisar_material, consultar_conteudo
from provas import gerar_atividade
from painel import mostrar_resumo


def menu_principal():
    if not carregar_dados():
        return

    # WHILE mantém o sistema aberto até a escolha de 0.
    while True:
        print("\n========================================")
        print("        ÁGORA - BIBLIOTECA ESCOLAR")
        print("========================================")
        print("\n1 - Adicionar material")
        print("2 - Gerenciar materiais")
        print("3 - Pesquisar material")
        print("4 - Gerar atividade")
        print("5 - Consultar conteúdo")
        print("6 - Resumo da biblioteca")
        print("0 - Sair")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            adicionar_material()
        elif opcao == "2":
            gerenciar_materiais()
        elif opcao == "3":
            pesquisar_material()
        elif opcao == "4":
            gerar_atividade()
        elif opcao == "5":
            consultar_conteudo()
        elif opcao == "6":
            mostrar_resumo()
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")



if __name__ == "__main__":
    menu_principal()
