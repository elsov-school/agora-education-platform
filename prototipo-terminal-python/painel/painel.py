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

def ler_atividades():
    """Lê provas/atividades.json sem alterá-lo e devolve a LISTA de atividades.

    Arquivo ausente, vazio ou inválido não derruba o painel: devolve [].
    """
    if not os.path.exists(ARQUIVO_ATIVIDADES):
        return []

    with open(ARQUIVO_ATIVIDADES, "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()

    if texto.strip() == "":
        return []

    try:
        atividades = json.loads(texto)
    except json.JSONDecodeError:
        print("Aviso: provas/atividades.json está inválido; as atividades não foram consideradas.")
        return []

    if not isinstance(atividades, list):
        print("Aviso: provas/atividades.json deve conter uma lista; as atividades não foram consideradas.")
        return []

    return atividades


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
    contagem = contar_atividades_por_disciplina(atividades)

    linhas = []
    for disciplina in contagem:
        linhas.append((disciplina, contagem[disciplina]))
    linhas.sort(key=lambda linha: (-linha[1], linha[0]))

    titulo_secao("ATIVIDADES GERADAS POR DISCIPLINA")
    if len(linhas) == 0:
        print("Nenhuma atividade registrada.")
        return
    for disciplina, total in linhas:
        print(f"{disciplina:<30} {total:>3}  ({percentual(total, len(atividades))})")
    print("\nTotal de atividades:", len(atividades))


def mostrar_materiais_mais_citados(atividades):
    ranking = listar_materiais_mais_citados(atividades, biblioteca.materiais)

    titulo_secao("MATERIAIS MAIS CITADOS COMO EVIDÊNCIA")
    if len(ranking) == 0:
        print("Nenhum material foi citado em atividades ainda.")
        return
    posicao = 1
    for material_id, titulo, total in ranking:
        palavra = "atividade" if total == 1 else "atividades"
        print(f"{posicao}º [{material_id}] {titulo} - citado em {total} {palavra}")
        posicao += 1
    print("\nObs.: as consultas entram nesta métrica quando o módulo de consultas registrar o uso.")


def mostrar_fila_pendentes():
    fila = listar_materiais_pendentes(biblioteca.materiais)
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


def mostrar_resumo():
    # DICIONÁRIOS de contagem, preenchidos a partir da LISTA de materiais.
    por_disciplina = {}
    por_serie = {}
    for material in biblioteca.materiais:
        disciplina = material["disciplina"]
        serie = material["serie"]
        if disciplina not in por_disciplina:
            por_disciplina[disciplina] = 0
        por_disciplina[disciplina] += 1
        if serie not in por_serie:
            por_serie[serie] = 0
        por_serie[serie] += 1

    titulo_secao("RESUMO DA BIBLIOTECA")
    print("Total de materiais:", len(biblioteca.materiais))
    print("\nMateriais por disciplina:")
    for disciplina in por_disciplina:
        print(disciplina + ": " + str(por_disciplina[disciplina]))
    print("\nMateriais por série:")
    for serie in por_serie:
        print(serie + ": " + str(por_serie[serie]))
    print("========================================")


def mostrar_painel_completo(atividades):
    professores_ativos = 0
    for usuario in ler_usuarios_por_id().values():
        if usuario["perfil"] == "professor" and usuario["ativo"]:
            professores_ativos += 1

    titulo_secao("PAINEL DA COORDENAÇÃO")
    print("Materiais na biblioteca:", len(biblioteca.materiais))
    print("Pendentes de validação: ", len(listar_materiais_pendentes(biblioteca.materiais)))
    print("Atividades geradas:     ", len(atividades))
    print("Professores ativos:     ", professores_ativos)

    mostrar_atividades_por_professor(atividades)
    mostrar_atividades_por_disciplina(atividades)
    mostrar_materiais_mais_citados(atividades)
    mostrar_fila_pendentes()


def menu_painel():
    """Abre o painel só para quem tem a permissão acessar_metricas (coordenação)."""
    texto = input("Seu ID de usuário: ").strip()
    if not texto.isdigit():
        print("O ID deve ser um número inteiro (ex: 1).")
        return
    if not cadastro.verificar_permissao(int(texto), "acessar_metricas"):
        print("Acesso negado: o painel é exclusivo da coordenação.")
        return

    # WHILE mantém o painel aberto até a escolha de 0.
    while True:
        print("\n========================================")
        print("        PAINEL DA COORDENAÇÃO")
        print("========================================")
        print("1 - Atividades por professor")
        print("2 - Atividades por disciplina")
        print("3 - Materiais mais citados como evidência")
        print("4 - Fila de materiais pendentes de validação")
        print("5 - Painel completo")
        print("6 - Resumo da biblioteca")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            break

        # Relê as atividades a cada escolha para mostrar sempre os dados atuais.
        atividades = ler_atividades()

        if opcao == "1":
            mostrar_atividades_por_professor(atividades)
        elif opcao == "2":
            mostrar_atividades_por_disciplina(atividades)
        elif opcao == "3":
            mostrar_materiais_mais_citados(atividades)
        elif opcao == "4":
            mostrar_fila_pendentes()
        elif opcao == "5":
            mostrar_painel_completo(atividades)
        elif opcao == "6":
            mostrar_resumo()
        else:
            print("Opção inválida.")


# Teste rápido, a partir da pasta prototipo-terminal-python:
#   python3 -m painel.painel   (Windows: py -m painel.painel)
if __name__ == "__main__":
    if biblioteca.carregar_dados():
        menu_painel()
