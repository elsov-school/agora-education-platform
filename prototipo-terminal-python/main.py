import json
import os


# TUPLAS: opções fixas que não mudam durante a execução.
BIMESTRES = (
    "1º Bimestre",
    "2º Bimestre",
    "3º Bimestre",
    "4º Bimestre"
)

DISCIPLINAS = (
    "Português",
    "Matemática",
    "Ciências",
    "História",
    "Geografia"
)

# LISTA: coleção dos materiais da biblioteca.
materiais = []

# O JSON fica sempre na mesma pasta deste programa.
ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados.json")


def materiais_exemplo():
    # Cada item desta lista é um DICIONÁRIO com os dados de um material.
    # Os códigos BNCC são ilustrativos para este protótipo acadêmico.
    return [
        {
            "id": 1,
            "titulo": "Sistema Solar",
            "disciplina": "Ciências",
            "serie": "6º ano",
            "bimestre": "1º Bimestre",
            "bncc": "EF06CI01",
            "conteudo": "O Sistema Solar é formado pelo Sol, oito planetas e outros corpos celestes. A Terra é um dos planetas e gira ao redor do Sol."
        },
        {
            "id": 2,
            "titulo": "Célula",
            "disciplina": "Ciências",
            "serie": "6º ano",
            "bimestre": "2º Bimestre",
            "bncc": "EF06CI05",
            "conteudo": "A célula é a unidade básica dos seres vivos. A membrana envolve a célula, e o citoplasma abriga estruturas que participam de suas funções."
        },
        {
            "id": 3,
            "titulo": "Equação do Primeiro Grau",
            "disciplina": "Matemática",
            "serie": "7º ano",
            "bimestre": "3º Bimestre",
            "bncc": "EF07MA18",
            "conteudo": "Uma equação do primeiro grau contém uma incógnita elevada à primeira potência. Para resolver x + 3 = 7, subtraímos 3 dos dois lados e encontramos x = 4."
        },
        {
            "id": 4,
            "titulo": "Gêneros Textuais",
            "disciplina": "Português",
            "serie": "6º ano",
            "bimestre": "4º Bimestre",
            "bncc": "EF06LP01",
            "conteudo": "Os gêneros textuais são formas de organizar textos conforme sua finalidade. Notícias informam acontecimentos, receitas orientam o preparo de alimentos e contos apresentam histórias."
        }
    ]


def carregar_dados():
    global materiais
    materiais = []

    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()

        if texto.strip() != "":
            try:
                materiais = json.loads(texto)
            except json.JSONDecodeError:
                print("Não foi possível ler dados.json: JSON inválido.")
                return False

            if not isinstance(materiais, list):
                print("dados.json deve conter uma lista de materiais.")
                return False

    if len(materiais) == 0:
        materiais = materiais_exemplo()
        salvar_dados()

    return True


def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(materiais, arquivo, ensure_ascii=False, indent=4)


def ler_texto(pergunta, valor_atual=""):
    while True:
        resposta = input(pergunta).strip()
        if resposta != "":
            return resposta
        elif valor_atual != "":
            return valor_atual
        else:
            print("Preencha este campo.")


def escolher_opcao(titulo, opcoes, valor_atual=""):
    print(titulo)
    for numero in range(len(opcoes)):
        print(str(numero + 1) + " - " + opcoes[numero])

    while True:
        resposta = input("Escolha uma opção: ").strip()
        if resposta == "" and valor_atual != "":
            return valor_atual
        try:
            numero = int(resposta)
        except ValueError:
            print("Digite um número válido.")
            continue

        if 1 <= numero <= len(opcoes):
            return opcoes[numero - 1]
        else:
            print("Opção inválida.")


def buscar_material_por_id(pergunta="ID: "):
    try:
        id_material = int(input(pergunta))
    except ValueError:
        print("Digite um número válido.")
        return None

    for material in materiais:
        if material["id"] == id_material:
            return material

    print("Material não encontrado.")
    return None


def adicionar_material():
    print("\n========================================")
    print("ADICIONAR MATERIAL")
    print("========================================")
    titulo = ler_texto("Título: ")
    disciplina = escolher_opcao("Disciplina:", DISCIPLINAS)
    serie = ler_texto("Série: ")
    bimestre = escolher_opcao("Bimestre:", BIMESTRES)
    bncc = ler_texto("Habilidade BNCC: ")
    conteudo = ler_texto("Conteúdo/descrição: ")

    maior_id = 0
    for item in materiais:
        if item["id"] > maior_id:
            maior_id = item["id"]

    # DICIONÁRIO: cada chave identifica uma informação do material.
    material = {
        "id": maior_id + 1,
        "titulo": titulo,
        "disciplina": disciplina,
        "serie": serie,
        "bimestre": bimestre,
        "bncc": bncc,
        "conteudo": conteudo
    }
    materiais.append(material)
    salvar_dados()
    print("Material cadastrado com sucesso!")


def listar_materiais():
    if len(materiais) == 0:
        print("Nenhum material cadastrado.")
        return

    for material in materiais:
        print("\nID:", material["id"])
        print("Título:", material["titulo"])
        print("Disciplina:", material["disciplina"])
        print("Série:", material["serie"])
        print("--------------------")


def mostrar_material(material):
    print("\nID:", material["id"])
    print("Título:", material["titulo"])
    print("Disciplina:", material["disciplina"])
    print("Série:", material["serie"])
    print("Bimestre:", material["bimestre"])
    print("Habilidade BNCC:", material["bncc"])
    print("Conteúdo:", material["conteudo"])


def visualizar_material():
    material = buscar_material_por_id()
    if material is not None:
        mostrar_material(material)


def editar_material():
    material = buscar_material_por_id()
    if material is None:
        return

    mostrar_material(material)
    print("\nPressione Enter para manter o valor atual de cada campo.")
    material["titulo"] = ler_texto("Título: ", material["titulo"])
    material["disciplina"] = escolher_opcao("Disciplina:", DISCIPLINAS, material["disciplina"])
    material["serie"] = ler_texto("Série: ", material["serie"])
    material["bimestre"] = escolher_opcao("Bimestre:", BIMESTRES, material["bimestre"])
    material["bncc"] = ler_texto("Habilidade BNCC: ", material["bncc"])
    material["conteudo"] = ler_texto("Conteúdo/descrição: ", material["conteudo"])
    salvar_dados()
    print("Material atualizado com sucesso!")


def excluir_material():
    material = buscar_material_por_id()
    if material is None:
        return

    mostrar_material(material)
    confirmacao = input("Tem certeza que deseja excluir? (s/n) ").strip().lower()
    if confirmacao == "s":
        materiais.remove(material)
        salvar_dados()
        print("Material excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


def gerenciar_materiais():
    while True:
        print("\n========================================")
        print("GERENCIAR MATERIAIS")
        print("========================================")
        listar_materiais()
        print("\n1 - Visualizar material")
        print("2 - Editar material")
        print("3 - Excluir material")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            visualizar_material()
        elif opcao == "2":
            editar_material()
        elif opcao == "3":
            excluir_material()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def pesquisar_material():
    termo = ler_texto("Digite o termo de pesquisa: ").lower()
    encontrou = False
    for material in materiais:
        if (termo in material["titulo"].lower()
                or termo in material["disciplina"].lower()
                or termo in material["serie"].lower()
                or termo in material["conteudo"].lower()
                or termo in material["bncc"].lower()):
            print("\n[" + str(material["id"]) + "] " + material["titulo"])
            print("Disciplina:", material["disciplina"])
            print("Série:", material["serie"])
            encontrou = True

    if not encontrou:
        print("Nenhum material encontrado.")


def gerar_atividade():
    listar_materiais()
    if len(materiais) == 0:
        return

    material = buscar_material_por_id("Digite o ID do material para gerar uma atividade: ")
    if material is None:
        return

    # LISTA de perguntas fixas: não há IA ou geração de respostas.
    perguntas = [
        'Qual é o tema principal do material "' + material["titulo"] + '"?',
        "Escreva três informações que você aprendeu com esse conteúdo.",
        "Explique com suas próprias palavras o assunto estudado.",
        "Qual parte do conteúdo você considera mais importante? Por quê?"
    ]
    print("\n========================================")
    print("ATIVIDADE")
    print("========================================")
    print("Material:", material["titulo"])
    print("Disciplina:", material["disciplina"])
    for numero in range(len(perguntas)):
        print("\n" + str(numero + 1) + ". " + perguntas[numero])
    print("\n========================================")


def consultar_conteudo():
    termo = ler_texto("Digite um assunto ou palavra que deseja consultar: ").lower()
    encontrou = False
    for material in materiais:
        if termo in material["conteudo"].lower():
            print("\n========================================")
            print("RESULTADO DA CONSULTA")
            print("========================================")
            print("Material:", material["titulo"])
            print("Disciplina:", material["disciplina"])
            print("\nConteúdo:")
            print(material["conteudo"])
            print("\nFonte:")
            print(material["titulo"] + " - " + material["disciplina"])
            print("========================================")
            encontrou = True

    if not encontrou:
        print("Não encontrei informações sobre esse assunto nos materiais cadastrados.")


def mostrar_resumo():
    # DICIONÁRIOS de contagem, preenchidos a partir da LISTA de materiais.
    por_disciplina = {}
    por_serie = {}
    for material in materiais:
        disciplina = material["disciplina"]
        serie = material["serie"]
        if disciplina not in por_disciplina:
            por_disciplina[disciplina] = 0
        por_disciplina[disciplina] += 1
        if serie not in por_serie:
            por_serie[serie] = 0
        por_serie[serie] += 1

    print("\n========================================")
    print("RESUMO DA BIBLIOTECA")
    print("========================================")
    print("Total de materiais:", len(materiais))
    print("\nMateriais por disciplina:")
    for disciplina in por_disciplina:
        print(disciplina + ": " + str(por_disciplina[disciplina]))
    print("\nMateriais por série:")
    for serie in por_serie:
        print(serie + ": " + str(por_serie[serie]))
    print("========================================")


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
