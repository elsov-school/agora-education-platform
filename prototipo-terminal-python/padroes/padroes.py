"""Padrões e exportação de provas em texto UTF-8."""

import os

MODELO_INSTITUCIONAL = {
    "nome": "institucional_v1",
    "cabecalho": [
        "Escola",
        "Disciplina",
        "Série",
        "Bimestre",
        "Professor",
    ],
    "campos": [
        "disciplina",
        "serie",
        "bimestre",
        "professor",
        "questoes",
    ],
    "regras": {
        "questoes_numeradas": True,
        "gabarito_separado": True,
        "ordenacao": "ordem_original",
    },
}


def obter_modelo(nome="institucional_v1"):
    """Retorna uma cópia do modelo solicitado."""
    if nome != MODELO_INSTITUCIONAL["nome"]:
        raise ValueError("Modelo de prova desconhecido: " + str(nome))

    return {
        "nome": MODELO_INSTITUCIONAL["nome"],
        "cabecalho": list(MODELO_INSTITUCIONAL["cabecalho"]),
        "campos": list(MODELO_INSTITUCIONAL["campos"]),
        "regras": dict(MODELO_INSTITUCIONAL["regras"]),
    }


def validar_prova(dados_prova):
    """Valida os dados obrigatórios da prova antes da formatação/exportação."""
    if not isinstance(dados_prova, dict):
        raise TypeError("Os dados da prova devem ser um dicionário.")

    campos_obrigatorios = (
        "disciplina",
        "serie",
        "bimestre",
        "questoes",
    )
    for campo in campos_obrigatorios:
        valor = dados_prova.get(campo)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            raise ValueError("Campo obrigatório ausente: " + campo)

    questoes = dados_prova["questoes"]
    if not isinstance(questoes, list) or len(questoes) == 0:
        raise ValueError("A prova deve conter ao menos uma questão.")

    for indice, questao in enumerate(questoes, 1):
        if not isinstance(questao, dict):
            raise TypeError("Questão " + str(indice) + " deve ser um dicionário.")

        enunciado = questao.get("enunciado")
        if not isinstance(enunciado, str) or not enunciado.strip():
            raise ValueError("Questão " + str(indice) + ": enunciado obrigatório.")

        gabarito = questao.get("gabarito")
        if gabarito is None or (isinstance(gabarito, str) and not gabarito.strip()):
            raise ValueError("Questão " + str(indice) + ": gabarito obrigatório.")

        criterio = questao.get("criterio_correcao")
        if criterio is None or (isinstance(criterio, str) and not criterio.strip()):
            raise ValueError(
                "Questão " + str(indice) + ": critério de correção obrigatório."
            )

    modelo = dados_prova.get("modelo_padrao", "institucional_v1")
    if modelo is not None:
        obter_modelo(modelo)

    return True


def formatar_prova(dados_prova, modelo):
    """Monta o texto da prova sem gravar o arquivo."""
    validar_prova(dados_prova)

    if isinstance(modelo, str):
        modelo = obter_modelo(modelo)
    elif not isinstance(modelo, dict):
        raise TypeError("Modelo inválido.")

    nome_modelo = modelo.get("nome", "institucional_v1")
    if nome_modelo != "institucional_v1":
        raise ValueError("Modelo de prova desconhecido: " + str(nome_modelo))

    linhas = [
        "=" * 40,
        "PROVA - ÁGORA",
        "=" * 40,
        "Escola: Ágora",
        "Disciplina: " + str(dados_prova["disciplina"]),
        "Série: " + str(dados_prova["serie"]),
        "Bimestre: " + str(dados_prova["bimestre"]),
    ]

    professor = dados_prova.get("professor")
    professor_id = dados_prova.get("professor_id")
    if professor is not None:
        linhas.append("Professor: " + str(professor))
    elif professor_id is not None:
        linhas.append("Professor ID: " + str(professor_id))

    linhas.extend(["", "QUESTÕES", "-" * 40])

    for numero, questao in enumerate(dados_prova["questoes"], 1):
        linhas.append(str(numero) + ". " + str(questao["enunciado"]))
        tipo = questao.get("tipo")
        dificuldade = questao.get("dificuldade")
        detalhes = []
        if tipo:
            detalhes.append("Tipo: " + str(tipo))
        if dificuldade:
            detalhes.append("Dificuldade: " + str(dificuldade))
        if detalhes:
            linhas.append("   " + " | ".join(detalhes))
        linhas.append("")

    linhas.append("=" * 40)
    return "\n".join(linhas)


def exportar_atividade(dados_prova, destino, incluir_gabarito=False):
    """Grava uma prova formatada em texto UTF-8 e retorna o caminho criado."""
    validar_prova(dados_prova)
    modelo = obter_modelo(dados_prova.get("modelo_padrao", "institucional_v1"))
    texto = formatar_prova(dados_prova, modelo)

    if incluir_gabarito:
        linhas = ["", "GABARITO", "-" * 40]
        for numero, questao in enumerate(dados_prova["questoes"], 1):
            linhas.append(str(numero) + ". " + str(questao["gabarito"]))
            criterio = questao.get("criterio_correcao")
            if criterio:
                linhas.append("   Critério: " + str(criterio))
        linhas.append("=" * 40)
        texto += "\n" + "\n".join(linhas)

    destino = os.path.expanduser(os.fspath(destino))
    if os.path.isdir(destino) or not os.path.splitext(destino)[1]:
        os.makedirs(destino, exist_ok=True)
        atividade_id = dados_prova.get("id")
        nome = (
            "atividade_" + str(atividade_id) + ".txt"
            if atividade_id is not None
            else "atividade.txt"
        )
        caminho = os.path.join(destino, nome)
    else:
        diretorio = os.path.dirname(os.path.abspath(destino))
        os.makedirs(diretorio, exist_ok=True)
        caminho = destino
        if not caminho.lower().endswith(".txt"):
            caminho += ".txt"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

    return caminho
