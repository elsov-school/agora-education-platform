"""CRUD 4 — Painel da Coordenação & Métricas. Contratos em painel/README.md.

Este módulo NÃO tem JSON próprio. Todas as métricas são consultas e
agregações feitas, somente leitura, sobre os dados dos outros CRUDs:

- usuarios/usuarios.json   (CRUD 1) -> nomes, perfis e permissões
- materiais/materiais.json (CRUD 2) -> biblioteca e status de validação
- provas/atividades.json   (CRUD 3) -> atividades geradas pelos professores
"""

import json
import os

from materiais import materiais as biblioteca
from usuarios import usuarios as cadastro

# O painel só LÊ o JSON de atividades; quem grava nele é provas.py.
PASTA_PROTOTIPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_ATIVIDADES = os.path.join(PASTA_PROTOTIPO, "provas", "atividades.json")

# TUPLA: valores fixos de status_validacao previstos no CRUD 2.
STATUS_VALIDACAO = ("pendente", "aprovado_coordenacao")
STATUS_PENDENTE = STATUS_VALIDACAO[0]


# ============================================================
# Leitura dos dados dos outros CRUDs (somente leitura)
# ============================================================

def ler_lista(caminho):
    """Lê um JSON do painel sem inicializar, migrar ou gravar o arquivo."""
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, list) or not all(isinstance(item, dict) for item in dados):
        raise ValueError(f"{os.path.basename(caminho)} deve conter uma lista de registros.")
    return dados


def ler_atividades():
    """Mantém o retorno de lista da consulta isolada de atividades."""
    try:
        return ler_lista(ARQUIVO_ATIVIDADES)
    except (OSError, ValueError) as erro:
        print("Não foi possível ler as atividades:", erro)
        return []


def ler_usuarios_por_id():
    """DICIONÁRIO {id: usuário}, montado a partir do CRUD de usuários."""
    usuarios_por_id = {}
    for usuario in cadastro.carregar_usuarios():
        usuarios_por_id[usuario["id"]] = usuario
    return usuarios_por_id


# ============================================================
# Funções do contrato (lógica, sem input/print)
# ============================================================

def contar_atividades_por_professor(atividades):
    """Agrupa as atividades por professor_id e devolve {professor_id: total}."""
    # DICIONÁRIO de contagem: chave = professor_id, valor = quantidade.
    contagem = {}
    for atividade in atividades:
        professor_id = atividade.get("professor_id")
        if professor_id not in contagem:
            contagem[professor_id] = 0
        contagem[professor_id] += 1
    return contagem


def contar_atividades_por_disciplina(atividades):
    """Agrupa as atividades por disciplina e devolve {disciplina: total}."""
    contagem = {}
    for atividade in atividades:
        disciplina = atividade.get("disciplina") or "Sem disciplina"
        if disciplina not in contagem:
            contagem[disciplina] = 0
        contagem[disciplina] += 1
    return contagem


def contar_atividades_por_serie(atividades):
    contagem = {}
    for atividade in atividades:
        serie = atividade.get("serie") or "Sem série"
        contagem[serie] = contagem.get(serie, 0) + 1
    return contagem


def listar_materiais_mais_usados(materiais):
    """Até três materiais com uso registrado, do maior total para o menor."""
    ranking = []
    for material in materiais:
        usos = material.get("usos", 0)
        if type(usos) is int and usos > 0:
            ranking.append((material["id"], material["titulo"], usos))
    ranking.sort(key=lambda item: (-item[2], item[1].casefold(), item[0]))
    return ranking[:3]


def listar_materiais_mais_citados(atividades, materiais):
    """Ranking dos materiais citados como referência (evidência) nas atividades.

    Devolve uma LISTA de TUPLAS (material_id, titulo, total), da mais citada
    para a menos citada; empates ficam em ordem alfabética. Um material
    repetido dentro da mesma atividade conta uma única vez.
    """
    citacoes = {}
    for atividade in atividades:
        # CONJUNTO (set): elimina IDs repetidos dentro da mesma atividade.
        for material_id in set(atividade.get("materiais_referenciados") or []):
            if material_id not in citacoes:
                citacoes[material_id] = 0
            citacoes[material_id] += 1

    titulos = {}
    for material in materiais:
        titulos[material["id"]] = material["titulo"]

    ranking = []
    for material_id in citacoes:
        titulo = titulos.get(material_id, "(material removido da biblioteca)")
        ranking.append((material_id, titulo, citacoes[material_id]))

    # Maior total primeiro (por isso o sinal de menos); empate -> título A-Z.
    ranking.sort(key=lambda item: (-item[2], item[1]))
    return ranking


def listar_materiais_pendentes(materiais):
    """Fila de materiais aguardando validação da coordenação, na ordem de cadastro.

    Material sem o campo status_validacao (cadastrado antes dessa evolução
    do CRUD 2) ainda não foi validado; por isso também entra na fila.
    """
    fila = []
    for material in materiais:
        if material.get("status_validacao", STATUS_PENDENTE) == STATUS_PENDENTE:
            fila.append(material)
    fila.sort(key=lambda material: material["id"])
    return fila


# ============================================================
# Interface no terminal (painel da coordenação)
# ============================================================

def titulo_secao(texto):
    print("\n========================================")
    print(texto)
    print("========================================")


def percentual(parte, total):
    if total == 0:
        return "0%"
    return str(round(parte / total * 100)) + "%"


def mostrar_atividades_por_professor(atividades):
    contagem = contar_atividades_por_professor(atividades)
    usuarios_por_id = ler_usuarios_por_id()

    # Professores ativos que ainda não geraram atividades aparecem com 0.
    for usuario in usuarios_por_id.values():
        if usuario["perfil"] == "professor" and usuario["ativo"] and usuario["id"] not in contagem:
            contagem[usuario["id"]] = 0

    # LISTA de TUPLAS (nome, total) para ordenar e exibir.
    linhas = []
    for professor_id in contagem:
        usuario = usuarios_por_id.get(professor_id)
        if usuario is None:
            nome = "ID " + str(professor_id) + " (não cadastrado)"
        elif not usuario["ativo"]:
            nome = usuario["nome"] + " (inativo)"
        else:
            nome = usuario["nome"]
        linhas.append((nome, contagem[professor_id]))
    linhas.sort(key=lambda linha: (-linha[1], linha[0]))

    titulo_secao("ATIVIDADES GERADAS POR PROFESSOR")
    if len(linhas) == 0:
        print("Nenhum professor ou atividade registrada.")
        return
    for nome, total in linhas:
        print(f"{nome:<30} {total:>3}  ({percentual(total, len(atividades))})")
    print("\nTotal de atividades:", len(atividades))


def mostrar_atividades_por_disciplina(atividades):
    mostrar_distribuicao("ATIVIDADES GERADAS POR DISCIPLINA",
                         contar_atividades_por_disciplina(atividades), len(atividades))


def mostrar_atividades_por_serie(atividades):
    mostrar_distribuicao("ATIVIDADES GERADAS POR SÉRIE",
                         contar_atividades_por_serie(atividades), len(atividades))


def mostrar_distribuicao(titulo, contagem, total_atividades):
    linhas = []
    for grupo in contagem:
        linhas.append((grupo, contagem[grupo]))
    linhas.sort(key=lambda linha: (-linha[1], linha[0]))

    titulo_secao(titulo)
    if len(linhas) == 0:
        print("Nenhuma atividade registrada.")
        return
    for grupo, total in linhas:
        print(f"{grupo:<30} {total:>3}  ({percentual(total, total_atividades)})")
    print("\nTotal de atividades:", total_atividades)


def mostrar_materiais_mais_citados(atividades, materiais=None):
    if materiais is None:
        materiais = biblioteca.materiais
    ranking = listar_materiais_mais_citados(atividades, materiais)

    titulo_secao("MATERIAIS MAIS CITADOS COMO EVIDÊNCIA")
    if len(ranking) == 0:
        print("Nenhum material foi citado em atividades ainda.")
        return
    posicao = 1
    for material_id, titulo, total in ranking:
        palavra = "atividade" if total == 1 else "atividades"
        print(f"{posicao}º [{material_id}] {titulo} - citado em {total} {palavra}")
        posicao += 1


def mostrar_materiais_mais_usados(materiais):
    titulo_secao("TOP 3 MATERIAIS POR USOS REGISTRADOS")
    ranking = listar_materiais_mais_usados(materiais)
    if not ranking:
        print("Nenhum uso registrado.")
    for posicao, (material_id, titulo, usos) in enumerate(ranking, start=1):
        print(f"{posicao}º [{material_id}] {titulo} - usos: {usos}")


def mostrar_fila_pendentes(materiais=None):
    if materiais is None:
        materiais = biblioteca.materiais
    fila = listar_materiais_pendentes(materiais)
    usuarios_por_id = ler_usuarios_por_id()

    titulo_secao("FILA DE MATERIAIS PENDENTES DE VALIDAÇÃO")
    if len(fila) == 0:
        print("Nenhum material aguardando validação.")
        return
    posicao = 1
    for material in fila:
        print(f"{posicao}. [{material['id']}] {material['titulo']} | "
              f"{material['disciplina']} | {material['serie']}")
        autor = material.get("autor_upload")
        if autor is not None:
            usuario = usuarios_por_id.get(autor)
            print("   Enviado por:", usuario["nome"] if usuario else autor)
        posicao += 1
    print(f"\n{len(fila)} material(is) aguardando a coordenação.")


def mostrar_resumo(materiais=None):
    if materiais is None:
        materiais = biblioteca.materiais
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

    titulo_secao("RESUMO DA BIBLIOTECA")
    print("Total de materiais:", len(materiais))
    print("Aprovados:", sum(1 for item in materiais if item.get("status_validacao") == "aprovado_coordenacao"))
    print("Pendentes:", len(listar_materiais_pendentes(materiais)))
    print("\nMateriais por disciplina:")
    for disciplina in por_disciplina:
        print(disciplina + ": " + str(por_disciplina[disciplina]))
    print("\nMateriais por série:")
    for serie in por_serie:
        print(serie + ": " + str(por_serie[serie]))
    print("========================================")


def mostrar_painel_completo(atividades, materiais=None):
    if materiais is None:
        materiais = biblioteca.materiais
    professores_ativos = 0
    for usuario in ler_usuarios_por_id().values():
        if usuario["perfil"] == "professor" and usuario["ativo"]:
            professores_ativos += 1

    titulo_secao("PAINEL DA COORDENAÇÃO")
    print("Atividades geradas:", len(atividades))
    print("Professores ativos:", professores_ativos)
    mostrar_resumo(materiais)
    mostrar_atividades_por_professor(atividades)
    mostrar_atividades_por_disciplina(atividades)
    mostrar_atividades_por_serie(atividades)
    mostrar_materiais_mais_usados(materiais)
    mostrar_materiais_mais_citados(atividades, materiais)
    mostrar_fila_pendentes(materiais)


def menu_painel(usuario=None):
    """Usa a sessão atual ou solicita um ID na execução isolada."""
    if usuario is None:
        try:
            usuario_id = int(input("Seu ID de usuário: ").strip())
        except ValueError:
            print("O ID deve ser um número inteiro.")
            return
    elif usuario.get("ativo") and usuario.get("perfil") == "coordenacao":
        usuario_id = usuario.get("id")
    else:
        print("Acesso negado: o painel é exclusivo da coordenação ativa.")
        return

    if not cadastro.verificar_permissao(usuario_id, "acessar_metricas"):
        print("Acesso negado: o painel é exclusivo da coordenação ativa.")
        return

    while True:
        titulo_secao("PAINEL DA COORDENAÇÃO")
        print("1 - Atividades por professor")
        print("2 - Atividades por disciplina")
        print("3 - Materiais citados como evidência em atividades")
        print("4 - Fila de materiais pendentes de validação")
        print("5 - Painel completo")
        print("6 - Resumo da biblioteca")
        print("7 - Atividades por série")
        print("8 - Top 3 materiais por usos")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if not cadastro.verificar_permissao(usuario_id, "acessar_metricas"):
            print("Acesso negado: o painel é exclusivo da coordenação ativa.")
            return

        try:
            if opcao in ("1", "2", "3", "5", "7"):
                atividades = ler_lista(ARQUIVO_ATIVIDADES)
            if opcao in ("3", "4", "5", "6", "8"):
                materiais = ler_lista(biblioteca.ARQUIVO_DADOS)
            if opcao == "1":
                mostrar_atividades_por_professor(atividades)
            elif opcao == "2":
                mostrar_atividades_por_disciplina(atividades)
            elif opcao == "3":
                mostrar_materiais_mais_citados(atividades, materiais)
            elif opcao == "4":
                mostrar_fila_pendentes(materiais)
            elif opcao == "5":
                mostrar_painel_completo(atividades, materiais)
            elif opcao == "6":
                mostrar_resumo(materiais)
            elif opcao == "7":
                mostrar_atividades_por_serie(atividades)
            elif opcao == "8":
                mostrar_materiais_mais_usados(materiais)
            else:
                print("Opção inválida.")
        except (OSError, ValueError, KeyError, TypeError) as erro:
            print("Não foi possível calcular a métrica:", erro)


if __name__ == "__main__":
    menu_painel()
