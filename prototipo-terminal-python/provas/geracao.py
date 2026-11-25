"""Geração local de questões de leitura e revisão de um rascunho."""

import re

TIPOS = ("multipla_escolha", "discursiva", "verdadeiro_falso")
DIFICULDADES = ("facil", "media", "dificil")


def questoes_do_material(material, tipo, dificuldade):
    texto = material.get("conteudo_texto") or material.get("conteudo") or ""
    questoes = []
    vistos = set()
    trechos = re.split(r"(?<=[.!?])\s+|\n+", texto.strip())
    for numero, trecho in enumerate(trechos, 1):
        trecho = trecho.strip()
        chave = " ".join(trecho.casefold().split()).rstrip(".!?")
        if not chave or chave in vistos:
            continue
        vistos.add(chave)
        questao = montar_questao(trecho, material["titulo"], numero, tipo, dificuldade, len(questoes))
        if questao:
            questao["tipo"] = tipo
            questao["dificuldade"] = dificuldade
            questoes.append(questao)
    return questoes


def montar_questao(trecho, titulo, numero, tipo, dificuldade, indice):
    palavras = list(re.finditer(r"\b\w+(?:[-’']\w+)*\b", trecho))
    if len(palavras) < 2:
        return None
    nivel = DIFICULDADES.index(dificuldade) + 1
    if tipo == "discursiva":
        tamanho_pista = min(4 - nivel, len(palavras) - 1)
        inicio = trecho[:palavras[tamanho_pista - 1].end()]
        return {
            "enunciado": (f'Leia o trecho {numero} de "{titulo}", que começa com «{inicio}…». '
                          "Explique sua ideia com suas próprias palavras."),
            "gabarito": trecho,
            "criterio_correcao": "Aceitar uma paráfrase que preserve a ideia do trecho.",
        }

    # A lacuna e as opções usam somente palavras do trecho original.
    lacuna = palavras[-1]
    resposta = lacuna.group()
    frase = trecho[:lacuna.start()] + "____" + trecho[lacuna.end():]
    outras = []
    vistas = {resposta.casefold()}
    for palavra in palavras:
        termo = palavra.group()
        if termo.casefold() not in vistas:
            outras.append(termo)
            vistas.add(termo.casefold())
        if len(outras) == nivel:
            break

    if tipo == "multipla_escolha":
        if not outras:
            return None
        alternativas = outras.copy()
        alternativas.insert(indice % (len(outras) + 1), resposta)
        return {
            "enunciado": f'Qual opção completa o trecho {numero} de "{titulo}" como no original? «{frase}»',
            "alternativas": alternativas,
            "gabarito": resposta,
            "criterio_correcao": "Marcar o termo que consta na lacuna do trecho original.",
        }

    pista = ""
    if dificuldade == "facil":
        pista = f" Pista: o termo original começa com «{resposta[0]}»."
    elif dificuldade == "media":
        pista = f" Pista: o termo original tem {len(resposta)} caracteres."
    termo = resposta
    gabarito = "Verdadeiro"
    if indice % 2 == 1 and outras:
        termo = outras[0]
        gabarito = "Falso"
    return {
        "enunciado": (f'No trecho {numero} de "{titulo}", «{frase}», a palavra que completa '
                      f'a lacuna no original é «{termo}». Verdadeiro ou falso?{pista}'),
        "gabarito": gabarito,
        "criterio_correcao": f"A palavra nessa posição do original é «{resposta}».",
    }


def questao_valida(questao):
    if not isinstance(questao, dict):
        return False
    for campo in ("enunciado", "tipo", "dificuldade", "gabarito", "criterio_correcao"):
        valor = questao.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            return False
    if questao["tipo"] not in TIPOS or questao["dificuldade"] not in DIFICULDADES:
        return False
    if questao["tipo"] == "multipla_escolha":
        opcoes = questao.get("alternativas")
        if not isinstance(opcoes, list) or len(opcoes) < 2:
            return False
        vistas = set()
        for opcao in opcoes:
            if not isinstance(opcao, str) or not opcao.strip():
                return False
            vistas.add(opcao.strip().casefold())
        return len(vistas) == len(opcoes) and questao["gabarito"] in opcoes
    if questao["tipo"] == "verdadeiro_falso":
        return questao["gabarito"].casefold() in ("verdadeiro", "falso", "v", "f")
    return True


def ler_numero(pergunta):
    try:
        return int(input(pergunta).strip())
    except ValueError:
        print("Digite um número inteiro.")
        return None


def mostrar_questao(numero, questao):
    print(f"\n{numero}. {questao['enunciado']}")
    print("Tipo:", questao["tipo"], "| Dificuldade:", questao["dificuldade"])
    for opcao in questao.get("alternativas", []):
        print("  -", opcao)
    print("Gabarito:", questao["gabarito"])
    print("Critério:", questao["criterio_correcao"])


def revisar_questao(questao):
    print("Pressione Enter para manter o valor exibido.")
    edicao = questao.copy()
    edicao["enunciado"] = input(f"Enunciado [{questao['enunciado']}]: ").strip() or questao["enunciado"]
    if questao.get("tipo") == "multipla_escolha":
        alternativas = []
        for alternativa in questao.get("alternativas", []):
            valor = input(f"Alternativa [{alternativa}]: ").strip()
            alternativas.append(valor or alternativa)
        edicao["alternativas"] = alternativas
    for campo, rotulo in (("gabarito", "Gabarito"), ("criterio_correcao", "Critério")):
        valor = input(f"{rotulo} [{questao[campo]}]: ").strip()
        edicao[campo] = valor or str(questao[campo])
    if questao_valida(edicao):
        return edicao
    print("Revisão inválida. Confira as alternativas e o gabarito.")
    return None


def editar_prova_gerada(prova):
    """Devolve o rascunho revisado ou None se o professor desistir."""
    revisada = prova.copy()
    questoes = list(prova["questoes"])
    revisada["questoes"] = questoes
    while True:
        print("\nRevisão da prova —", prova["disciplina"], "|", prova["serie"])
        for numero, questao in enumerate(questoes, 1):
            mostrar_questao(numero, questao)
        print("1 - Aprovar para salvar   2 - Editar questão   0 - Descartar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return None
        if opcao == "1":
            return revisada
        if opcao == "2":
            numero = ler_numero("Número da questão: ")
            if numero is not None and 1 <= numero <= len(questoes):
                editada = revisar_questao(questoes[numero - 1])
                if editada:
                    questoes[numero - 1] = editada
            else:
                print("Número de questão inválido.")
        else:
            print("Opção inválida.")
