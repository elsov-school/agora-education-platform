"""Funcionalidades existentes; evoluções descritas em provas/README.md."""
import json
import os
from datetime import datetime

from materiais import materiais as biblioteca

atividades = []

CAMPOS_QUESTAO = [
    "enunciado",
    "tipo",
    "dificuldade",
    "gabarito",
    "criterio_correcao"
]

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atividades.json")

def carregar_atividades():
    global atividades

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        atividades = json.load(arquivo)

def salvar_atividades():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(atividades, arquivo, ensure_ascii=False, indent=4)

def verificar_autoria(atividade, professor_id):
    return atividade["professor_id"] == professor_id

def editar_questao(professor_id, atividade_id, indice_questao, dados_questao):
    carregar_atividades()
    atividade_encontrada = None

    for atividade in atividades:
        if atividade["id"] == atividade_id:
            atividade_encontrada = atividade

    if atividade_encontrada is None:
        print("Atividade não encontrada.")
        return

    if not verificar_autoria(atividade_encontrada, professor_id):
        print("Você não tem permissão para editar esta atividade.")
        return

    if (
            type(indice_questao) is not int
            or indice_questao >= len(atividade_encontrada["questoes"])
            or indice_questao < 0
    ):
        print("O índice da questão é inválido.")
        return

    if not isinstance(dados_questao, dict):
        print("A questão deve ser enviada em formato de dicionário.")
        return

    for campo in CAMPOS_QUESTAO:
        if campo not in dados_questao:
            print(f"Campo obrigatório ausente: {campo}")
            return

        if not dados_questao[campo]:
            print(f"Campo obrigatório vazio: {campo}")
            return

    atividade_encontrada["questoes"][indice_questao] = dados_questao
    salvar_atividades()
    print("Questão editada com sucesso!")

def listar_historico(professor_id):
    carregar_atividades()
    historico = []

    # Filtra apenas as atividades do professor
    for atividade in atividades:
        if verificar_autoria(atividade, professor_id):
            historico.append(atividade)

    # Verifica se existe algum registro
    if len(historico) == 0:
        print("Nenhuma atividade encontrada para este professor.")
        return

    # Ordena da atividade mais recente para a mais antiga
    historico.sort(
        key=lambda atividade: datetime.strptime(
            atividade["data_criacao"], "%d/%m/%Y %H:%M"
        ),
        reverse=True
    )

    # Exibe o histórico
    print("\n===== HISTÓRICO DE ATIVIDADES =====")

    for atividade in historico:
        print(f"ID: {atividade['id']}")
        print(f"Série: {atividade['serie']}")
        print(f"Disciplina: {atividade['disciplina']}")
        print(f"Bimestre: {atividade['bimestre']}")
        print(f"Data de criação: {atividade['data_criacao']}")
        print("-" * 40)

def excluir_prova(atividade_id, professor_id):
    carregar_atividades()
    atividade_encontrada = None

    for atividade in atividades:
        if atividade["id"] == atividade_id:
            atividade_encontrada = atividade

    if atividade_encontrada is None:
        print("Atividade não encontrada.")
        return

    if not verificar_autoria(atividade_encontrada, professor_id):
        print("Você não tem permissão para excluir esta atividade.")
        return

    confirmacao = input("Tem certeza que deseja excluir esta prova? (s/n): ").strip().lower()

    if confirmacao != "s":
        print("Exclusão cancelada.")
        return

    atividades.remove(atividade_encontrada)
    salvar_atividades()

    print("Prova excluída com sucesso!")

def salvar_prova(professor_id, dados_prova):
    carregar_atividades()

    if not isinstance(dados_prova, dict):
        print("Os dados da prova devem ser enviados em formato de dicionário.")
        return

    campos_obrigatorios = [
        "serie",
        "disciplina",
        "bimestre",
        "materiais_referenciados",
        "questoes",
        "modelo_padrao"
    ]

    for campo in campos_obrigatorios:
        if campo not in dados_prova:
            print(f"Campo obrigatório ausente: {campo}")
            return

        if not dados_prova[campo]:
            print(f"Campo obrigatório vazio: {campo}")
            return

    if not isinstance(dados_prova["materiais_referenciados"], list):
        print("Os materiais referenciados devem ser enviados em formato de lista.")
        return

    if not isinstance(dados_prova["questoes"], list):
        print("As questões devem ser enviadas em formato de lista.")
        return

    for questao in dados_prova["questoes"]:

        if not isinstance(questao, dict):
            print("Cada questão deve ser enviada em formato de dicionário.")
            return

        for campo in CAMPOS_QUESTAO:
            if campo not in questao:
                print(f"Campo obrigatório ausente na questão: {campo}")
                return

            if not questao[campo]:
                print(f"Campo obrigatório vazio na questão: {campo}")
                return

    for id_material in dados_prova["materiais_referenciados"]:
        material_encontrado = False

        for material in biblioteca.materiais:
            if material["id"] == id_material:
                material_encontrado = True

        if not material_encontrado:
            print(f"ID do Material ausente: {id_material}")
            return

    ids = []

    for atividade in atividades:
        ids.append(atividade["id"])

    if len(ids) == 0:
        novo_id = 1
    else:
        novo_id = max(ids) + 1

    data_criacao = datetime.now().strftime("%d/%m/%Y %H:%M")

    nova_atividade = {
        "id": novo_id,
        "professor_id": professor_id,
        "serie": dados_prova["serie"],
        "disciplina": dados_prova["disciplina"],
        "bimestre": dados_prova["bimestre"],
        "materiais_referenciados": dados_prova["materiais_referenciados"],
        "questoes": dados_prova["questoes"],
        "data_criacao": data_criacao,
        "modelo_padrao": dados_prova["modelo_padrao"]
    }

    atividades.append(nova_atividade)
    salvar_atividades()



def gerar_atividade ():
    biblioteca.listar_materiais ()
    if len (biblioteca.materiais )==0 :
        return

    material =biblioteca.buscar_material_por_id ("Digite o ID do material para gerar uma atividade: ")
    if material is None :
        return

        # LISTA de perguntas fixas: não há IA ou geração de respostas.
    perguntas =[
    'Qual é o tema principal do material "'+material ["titulo"]+'"?',
    "Escreva três informações que você aprendeu com esse conteúdo.",
    "Explique com suas próprias palavras o assunto estudado.",
    "Qual parte do conteúdo você considera mais importante? Por quê?"
    ]
    print ("\n========================================")
    print ("ATIVIDADE")
    print ("========================================")
    print ("Material:",material ["titulo"])
    print ("Disciplina:",material ["disciplina"])
    for numero in range (len (perguntas )):
        print ("\n"+str (numero +1 )+". "+perguntas [numero ])
    print ("\n========================================")

if __name__ == "__main__":
    dados_teste = {
        "serie": "7º Ano",
        "disciplina": "Matemática",
        "bimestre": "1º Bimestre",
        "materiais_referenciados": [1],
        "questoes": [
            {
                "enunciado": "Quanto é 2 + 2?",
                "tipo": "discursiva",
                "dificuldade": "facil",
                "gabarito": "4",
                "criterio_correcao": "Resposta correta: 4"
            }
        ],
        "modelo_padrao": "institucional_v1"
    }

    dados_questao_teste = {
        "enunciado": "Quanto é 5 + 5?",
        "tipo": "discursiva",
        "dificuldade": "facil",
        "gabarito": "10",
        "criterio_correcao": "Resposta correta: 10"
    }

    biblioteca.carregar_dados()

    #salvar_prova(1, dados_teste)

    #editar_questao(1, 1, 0, dados_questao_teste)

    #excluir_prova(4, 1)
    #listar_historico(1)

    #print(atividades)
