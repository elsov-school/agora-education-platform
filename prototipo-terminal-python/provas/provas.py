"""Funcionalidades existentes; evoluções descritas em provas/README.md."""
import json
import os
from datetime import datetime

from materiais import materiais as biblioteca

atividades = []

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atividades.json")

def carregar_atividades():
    global atividades

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
        atividades = json.load(arquivo)

def salvar_atividades():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(atividades, arquivo, ensure_ascii=False, indent=4)


def salvar_prova(professor_id, dados_prova):
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

    if not isinstance(dados_prova["questoes"], list):
        print("As questões devem ser enviadas em formato de lista.")
        return

    campos_questao = [
        "enunciado",
        "tipo",
        "dificuldade",
        "gabarito",
        "criterio_correcao"
    ]

    for questao in dados_prova["questoes"]:

        if not isinstance(questao, dict):
            print("Cada questão deve ser enviada em formato de dicionário.")
            return

        for campo in campos_questao:
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

    carregar_atividades()

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

    biblioteca.carregar_dados()
    salvar_prova(1, dados_teste)

    print(atividades)
