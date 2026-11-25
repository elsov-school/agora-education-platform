"""Padrão institucional e exportação de provas em texto UTF-8."""

import json
import os
import shutil
import tempfile

from usuarios import usuarios

PASTA_MODULO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_REGRAS = os.path.join(PASTA_MODULO, "regras.json")
PASTA_EXPORTACOES = os.path.join(os.path.dirname(PASTA_MODULO), "exportacoes")

MODELO_INSTITUCIONAL = {
    "nome": "institucional_v1",
    "cabecalho": ["Escola", "Disciplina", "Série", "Bimestre", "Professor"],
    "campos": ["disciplina", "serie", "bimestre", "professor", "questoes"],
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


def _tem_texto(valor):
    return isinstance(valor, str) and bool(valor.strip())


def carregar_regras():
    """Lê e valida as regras vigentes da escola."""
    with open(ARQUIVO_REGRAS, encoding="utf-8") as arquivo:
        try:
            regras = json.load(arquivo)
        except ValueError as erro:
            raise ValueError("O arquivo de regras não contém JSON UTF-8 válido.") from erro

    if not isinstance(regras, dict):
        raise ValueError("O arquivo de regras deve conter um objeto JSON.")
    for campo in ("nome_escola", "instrucoes"):
        if not _tem_texto(regras.get(campo)):
            raise ValueError("Texto obrigatório nas regras: " + campo)
    limite = regras.get("max_questoes")
    if type(limite) is not int or limite <= 0:
        raise ValueError("O limite de questões deve ser um inteiro positivo.")
    return regras


def _gravar_texto(caminho, texto):
    """Substitui o arquivo somente depois de concluir a escrita."""
    pasta = os.path.dirname(os.path.abspath(caminho))
    with tempfile.TemporaryDirectory(dir=pasta) as temporaria:
        rascunho = os.path.join(temporaria, "rascunho")
        with open(rascunho, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)
        os.replace(rascunho, caminho)


def _coordenacao_ativa(usuario):
    return (isinstance(usuario, dict) and usuario.get("perfil") == "coordenacao"
            and usuario.get("ativo") is True)


def configurar_padrao_escola(usuario):
    """Edita as regras no terminal usando a sessão da coordenação."""
    try:
        if not _coordenacao_ativa(usuario) or type(usuario.get("id")) is not int:
            print("Somente a coordenação ativa pode configurar o padrão da escola.")
            return None
        cadastro = usuarios.buscar_usuario(usuarios.carregar_usuarios(), usuario["id"])
        if not _coordenacao_ativa(cadastro):
            print("O cadastro atual não permite configurar o padrão da escola.")
            return None
        regras = carregar_regras()
        print("Pressione Enter para manter o valor atual de cada campo.")
        nome = input(f"Nome da escola [{regras['nome_escola']}]: ").strip()
        limite = input(f"Máximo de questões [{regras['max_questoes']}]: ").strip()
        if limite:
            if not limite.isdecimal() or int(limite) <= 0:
                raise ValueError("O limite de questões deve ser um inteiro positivo.")
            regras["max_questoes"] = int(limite)
        instrucoes = input(f"Instruções [{regras['instrucoes']}]: ").strip()
        if nome:
            regras["nome_escola"] = nome
        if instrucoes:
            regras["instrucoes"] = instrucoes

        _gravar_texto(ARQUIVO_REGRAS, json.dumps(regras, ensure_ascii=False, indent=2) + "\n")
    except (ValueError, OSError, KeyError, TypeError) as erro:
        print("Não foi possível configurar o padrão da escola:", erro)
        return None

    print("Padrão da escola salvo.")
    return regras


def _validar_questao(questao, numero, exigir_detalhes):
    inicio = f"Questão {numero}: "
    if not isinstance(questao, dict):
        raise TypeError(inicio + "deve ser um dicionário.")
    if not _tem_texto(questao.get("enunciado")):
        raise ValueError(inicio + "enunciado obrigatório.")
    gabarito = questao.get("gabarito")
    if not (_tem_texto(gabarito) or isinstance(gabarito, (int, float))):
        raise ValueError(inicio + "gabarito obrigatório.")
    if not _tem_texto(questao.get("criterio_correcao")):
        raise ValueError(inicio + "critério de correção obrigatório.")
    for campo in ("tipo", "dificuldade"):
        if (exigir_detalhes or campo in questao) and not _tem_texto(questao.get(campo)):
            raise ValueError(inicio + campo + " obrigatório.")

    tipo = questao.get("tipo", "").strip().lower().replace("ú", "u")
    tipo = tipo.replace("_", " ").replace("-", " ")
    alternativas = questao.get("alternativas", [])
    if not isinstance(alternativas, list):
        raise ValueError(inicio + "as alternativas devem formar uma lista.")
    if tipo in ("multipla escolha", "multipla") and len(alternativas) < 2:
        raise ValueError(inicio + "informe ao menos duas alternativas.")
    for alternativa in alternativas:
        if not _tem_texto(alternativa):
            raise ValueError(inicio + "cada alternativa deve conter texto.")


def _validar_prova(dados_prova, regras, exigir_detalhes=False):
    if not isinstance(dados_prova, dict):
        raise TypeError("Os dados da prova devem ser um dicionário.")
    for campo in ("disciplina", "serie", "bimestre"):
        valor = dados_prova.get(campo)
        if not (_tem_texto(valor) or (campo != "disciplina" and type(valor) is int)):
            raise ValueError("Campo obrigatório ausente ou inválido: " + campo)

    questoes = dados_prova.get("questoes")
    if not isinstance(questoes, list) or not questoes:
        raise ValueError("A prova deve conter ao menos uma questão.")
    if len(questoes) > regras["max_questoes"]:
        raise ValueError(f"A prova excede o limite de {regras['max_questoes']} questões.")
    for numero, questao in enumerate(questoes, 1):
        _validar_questao(questao, numero, exigir_detalhes)
    modelo = dados_prova.get("modelo_padrao")
    if modelo is not None:
        obter_modelo(modelo)


def validar_prova(dados_prova):
    """Confere o limite institucional e os campos usados na formatação."""
    _validar_prova(dados_prova, carregar_regras())
    return True


def _cabecalho(titulo, prova, regras):
    linhas = [
        "=" * 40, titulo, "=" * 40,
        "Escola: " + regras["nome_escola"],
        "Disciplina: " + prova["disciplina"],
        "Série: " + str(prova["serie"]),
        "Bimestre: " + str(prova["bimestre"]),
    ]
    if prova.get("professor") is not None:
        linhas.append("Professor: " + str(prova["professor"]))
    elif prova.get("professor_id") is not None:
        linhas.append("Professor ID: " + str(prova["professor_id"]))
    return linhas


def _texto_aluno(prova, regras):
    linhas = _cabecalho("PROVA - " + regras["nome_escola"].upper(), prova, regras)
    linhas.extend(["Instruções: " + regras["instrucoes"], "", "QUESTÕES", "-" * 40])
    for numero, questao in enumerate(prova["questoes"], 1):
        linhas.append(f"{numero}. {questao['enunciado']}")
        detalhes = []
        if questao.get("tipo"):
            detalhes.append("Tipo: " + questao["tipo"])
        if questao.get("dificuldade"):
            detalhes.append("Dificuldade: " + questao["dificuldade"])
        if detalhes:
            linhas.append("   " + " | ".join(detalhes))
        for indice, alternativa in enumerate(questao.get("alternativas", [])):
            letra = chr(ord("A") + indice) if indice < 26 else str(indice + 1)
            if alternativa.upper().startswith((letra + ")", letra + ".")):
                linhas.append("   " + alternativa)
            else:
                linhas.append(f"   {letra}) {alternativa}")
        linhas.append("")
    linhas.append("=" * 40)
    return "\n".join(linhas)


def formatar_prova(dados_prova, modelo):
    """Monta o texto destinado ao aluno, sem gravar arquivo."""
    if isinstance(modelo, dict):
        modelo = modelo.get("nome", "institucional_v1")
    if not isinstance(modelo, str):
        raise TypeError("Modelo inválido.")
    obter_modelo(modelo)
    regras = carregar_regras()
    _validar_prova(dados_prova, regras)
    return _texto_aluno(dados_prova, regras)


def _linhas_gabarito(prova):
    linhas = []
    for numero, questao in enumerate(prova["questoes"], 1):
        linhas.append(f"{numero}. {questao['gabarito']}")
        linhas.append("   Critério: " + questao["criterio_correcao"])
    linhas.append("=" * 40)
    return linhas


def _id_para_arquivo(atividade_id):
    texto = str(atividade_id)
    if not texto.isascii() or not texto.isdecimal() or int(texto) <= 0:
        raise ValueError("Informe o ID numérico positivo da prova salva.")
    return texto


def exportar_prova_formatada(prova, destino=None):
    """Gera a prova do aluno e o gabarito do professor, nessa ordem."""
    regras = carregar_regras()
    _validar_prova(prova, regras, exigir_detalhes=True)
    atividade_id = _id_para_arquivo(prova.get("id"))
    pasta = PASTA_EXPORTACOES if destino is None else os.path.expanduser(os.fspath(destino))
    aluno = os.path.join(pasta, f"prova_aluno_{atividade_id}.txt")
    professor = os.path.join(pasta, f"gabarito_professor_{atividade_id}.txt")
    texto_aluno = _texto_aluno(prova, regras)
    gabarito = _cabecalho("GABARITO DO PROFESSOR", prova, regras)
    gabarito.extend(["", "GABARITO", "-" * 40])
    gabarito.extend(_linhas_gabarito(prova))

    os.makedirs(pasta, exist_ok=True)
    # Uma exportação por ID de cada vez, para manter as duas versões juntas.
    preparo = os.path.join(pasta, ".exportando_" + atividade_id)
    os.mkdir(preparo)
    try:
        novo_aluno = os.path.join(preparo, "aluno.txt")
        novo_professor = os.path.join(preparo, "professor.txt")
        with open(novo_aluno, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto_aluno)
        with open(novo_professor, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(gabarito))

        anterior = os.path.join(preparo, "aluno_anterior")
        tinha_aluno = os.path.isfile(aluno)
        if tinha_aluno:
            shutil.copyfile(aluno, anterior)
        os.replace(novo_aluno, aluno)
        try:
            os.replace(novo_professor, professor)
        except OSError:
            if tinha_aluno:
                os.replace(anterior, aluno)
            else:
                os.remove(aluno)
            raise
    finally:
        shutil.rmtree(preparo)
    return [aluno, professor]


def exportar_atividade(dados_prova, destino, incluir_gabarito=False):
    """Grava um único arquivo, preservando a interface anterior."""
    texto = formatar_prova(dados_prova, "institucional_v1")
    if incluir_gabarito:
        linhas = ["", "GABARITO", "-" * 40] + _linhas_gabarito(dados_prova)
        texto += "\n" + "\n".join(linhas)

    destino = os.path.expanduser(os.fspath(destino))
    if os.path.isdir(destino) or not os.path.splitext(destino)[1]:
        nome = "atividade.txt"
        if dados_prova.get("id") is not None:
            nome = "atividade_" + _id_para_arquivo(dados_prova["id"]) + ".txt"
        caminho = os.path.join(destino, nome)
    else:
        caminho = destino if destino.lower().endswith(".txt") else destino + ".txt"
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    _gravar_texto(caminho, texto)
    return caminho
