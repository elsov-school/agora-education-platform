"""Pesquisa e consulta de trechos da biblioteca aprovada."""

from materiais import materiais as biblioteca
from usuarios import usuarios


def _ler_termo(usuario, pergunta):
    if not usuario or usuario.get("ativo") is not True:
        print("Faça login com um usuário ativo para consultar os materiais.")
        return None
    return biblioteca.ler_texto(pergunta).lower()


def _materiais_aprovados(usuario):
    try:
        if biblioteca.carregar_dados() is False:
            print("Não foi possível consultar a biblioteca.")
            return None
        permitidos = usuarios.filtrar_materiais_do_professor(usuario, biblioteca.materiais)
    except (OSError, ValueError):
        print("Não foi possível ler os dados da biblioteca ou do usuário.")
        return None

    # A coordenação pode ver pendências na biblioteca, mas só há consulta de aprovados.
    aprovados = []
    for material in permitidos:
        if material.get("status_validacao") == "aprovado_coordenacao":
            aprovados.append(material)
    return aprovados


def _conteudo(material):
    return material.get("conteudo_texto", material.get("conteudo", ""))


def _habilidade(material):
    return material.get("habilidade_bncc", material.get("bncc", ""))


def pesquisar_material(usuario=None):
    """Lista fontes permitidas que contêm o termo, sem registrar uso."""
    termo = _ler_termo(usuario, "Digite o termo de pesquisa: ")
    if termo is None:
        return
    materiais = _materiais_aprovados(usuario)
    if materiais is None:
        return

    encontrou = False
    for material in materiais:
        campos = (material["titulo"], material["disciplina"], material["serie"],
                  _conteudo(material), _habilidade(material))
        for campo in campos:
            if termo in campo.lower():
                print(f"\n[{material['id']}] {material['titulo']}")
                print("Disciplina:", material["disciplina"])
                print("Série:", material["serie"])
                encontrou = True
                break
    if not encontrou:
        print("Nenhum material encontrado na base aprovada disponível para este usuário.")


def _trecho_literal(material, termo):
    for linha in _conteudo(material).splitlines():
        if termo in linha.lower():
            return linha
    return None


def consultar_com_evidencia(usuario):
    """Exibe a primeira linha com o termo e registra um uso por fonte encontrada."""
    termo = _ler_termo(usuario, "Digite um assunto ou palavra que deseja consultar: ")
    if termo is None:
        return
    materiais = _materiais_aprovados(usuario)
    if materiais is None:
        return

    encontrou = False
    for material in materiais:
        linha = _trecho_literal(material, termo)
        if linha is None:
            continue
        print(f"\nFonte: [{material['id']}] {material['titulo']}")
        print("Disciplina:", material["disciplina"])
        print("Série:", material["serie"])
        print("Habilidade BNCC:", _habilidade(material) or "Não informada")
        print("Trecho literal:")
        print(linha)
        encontrou = True
        try:
            registrado = biblioteca.registrar_uso(material["id"])
        except (OSError, ValueError):
            registrado = False
        if registrado is False:
            print("Não foi possível registrar o uso deste material.")
    if not encontrou:
        print("Nenhum trecho encontrado na base aprovada disponível para este usuário.")


def consultar_conteudo(usuario=None):
    """Entrada do menu para a consulta com evidência."""
    consultar_com_evidencia(usuario)
