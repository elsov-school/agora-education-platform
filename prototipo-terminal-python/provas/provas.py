"""Criação, revisão e histórico de avaliações no terminal."""

import json
import os
from datetime import datetime

from materiais import materiais as biblioteca
from padroes import padroes
from usuarios import usuarios
from provas.geracao import (
    DIFICULDADES, TIPOS, editar_prova_gerada, ler_numero, mostrar_questao,
    questao_valida, questoes_do_material, revisar_questao,
)

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atividades.json")


def _ler_atividades():
    try:
        with open(ARQUIVO_DADOS, encoding="utf-8") as arquivo:
            registros = json.load(arquivo)
        if not isinstance(registros, list):
            raise ValueError("era esperada uma lista")
        ids = set()
        for registro in registros:
            if not isinstance(registro, dict):
                raise ValueError("registro de prova inválido")
            numero = registro.get("id")
            if type(numero) is not int or numero < 1 or numero in ids:
                raise ValueError("ID inválido ou duplicado")
            ids.add(numero)
            if type(registro.get("professor_id")) is not int or not isinstance(registro.get("questoes"), list):
                raise ValueError(f"autoria ou questões inválidas na prova {numero}")
            for questao in registro["questoes"]:
                if not isinstance(questao, dict):
                    raise ValueError(f"questão inválida na prova {numero}")
                for campo in ("enunciado", "tipo", "dificuldade", "criterio_correcao"):
                    if not isinstance(questao.get(campo), str):
                        raise ValueError(f"campo {campo} inválido na prova {numero}")
                if not isinstance(questao.get("gabarito"), (str, int, float)):
                    raise ValueError(f"gabarito inválido na prova {numero}")
                if not isinstance(questao.get("alternativas", []), list):
                    raise ValueError(f"alternativas inválidas na prova {numero}")
        return registros
    except (OSError, ValueError) as erro:
        print("Não foi possível ler o histórico de provas:", erro)
        return None


def _gravar_atividades(anteriores, novas):
    # O modo exclusivo reserva a escrita. A comparação impede salvar uma revisão antiga.
    temporario = ARQUIVO_DADOS + ".tmp"
    try:
        arquivo = open(temporario, "x", encoding="utf-8")
    except FileExistsError:
        print("Há uma gravação de provas em andamento. Tente novamente.")
        return False
    except OSError as erro:
        print("Não foi possível iniciar a gravação:", erro)
        return False
    publicada = False
    try:
        with arquivo:
            if anteriores != _ler_atividades():
                print("O histórico mudou. Consulte-o novamente.")
                return False
            json.dump(novas, arquivo, ensure_ascii=False, indent=4)
        os.replace(temporario, ARQUIVO_DADOS)
        publicada = True
        return True
    except (OSError, TypeError, ValueError) as erro:
        print("Não foi possível gravar o histórico de provas:", erro)
        return False
    finally:
        if not publicada:
            try:
                os.remove(temporario)
            except OSError as erro:
                print("Não foi possível remover o arquivo temporário:", erro)


def _usuario_ativo(usuario):
    if isinstance(usuario, dict) and usuario.get("ativo") is True and type(usuario.get("id")) is int:
        try:
            atual = usuarios.buscar_usuario(usuarios.carregar_usuarios(), usuario["id"])
            if atual and atual.get("ativo") is True and atual.get("perfil") == usuario.get("perfil"):
                if atual["perfil"] in ("professor", "coordenacao"):
                    return atual
        except (OSError, ValueError, TypeError, KeyError) as erro:
            print("Não foi possível consultar usuários:", erro)
    print("Entre com um usuário ativo para acessar as provas.")
    return None


def verificar_autoria(atividade, professor_id):
    return atividade["professor_id"] == professor_id


def _atividade_permitida(registros, atividade_id, usuario):
    if registros is None or usuario is None:
        return None
    for atividade in registros:
        if type(atividade_id) is int and atividade["id"] == atividade_id:
            if usuario["perfil"] == "coordenacao" or verificar_autoria(atividade, usuario["id"]):
                return atividade
            break
    print("Prova indisponível para este usuário.")
    return None


def _materiais_aprovados(usuario):
    if not hasattr(usuarios, "filtrar_materiais_do_professor"):
        print("A seleção de materiais requer o módulo de usuários do contrato v1.")
        return []
    try:
        if biblioteca.carregar_dados() is False:
            return []
        permitidos = usuarios.filtrar_materiais_do_professor(usuario, biblioteca.materiais)
        return [m for m in permitidos if m.get("status_validacao") == "aprovado_coordenacao"]
    except (OSError, ValueError) as erro:
        print("Não foi possível carregar a biblioteca:", erro)
        return []


def _limite_questoes():
    if not hasattr(padroes, "carregar_regras"):
        print("A geração de provas requer as regras do módulo de padrões do contrato v1.")
        return 0
    try:
        limite = padroes.carregar_regras()["max_questoes"]
        if type(limite) is int and limite > 0:
            return limite
    except (OSError, ValueError, TypeError, KeyError) as erro:
        print("Não foi possível carregar as regras:", erro)
    print("O limite de questões deve ser um inteiro positivo.")
    return 0


def _referencias_permitidas(dados, usuario):
    referencias = dados.get("materiais_referenciados")
    if not isinstance(referencias, list) or not referencias:
        print("Informe os IDs dos materiais usados.")
        return []
    permitidos = {m["id"]: m for m in _materiais_aprovados(usuario)}
    ids = []
    for numero in referencias:
        if type(numero) is not int or numero not in permitidos:
            print("Material indisponível para esta prova:", numero)
            return []
        material = permitidos[numero]
        for campo in ("disciplina", "serie", "bimestre"):
            if dados[campo] != material.get(campo):
                print("O material não corresponde ao campo da prova:", campo)
                return []
        if numero not in ids:
            ids.append(numero)
    return ids


def salvar_prova(professor_id, dados_prova, usuario=None):
    """Salva a prova revisada com a autoria da sessão e devolve o registro gravado."""
    autor = _usuario_ativo(usuario)
    if not autor or type(professor_id) is not int or autor["id"] != professor_id:
        print("A autoria deve corresponder ao usuário da sessão.")
        return None
    if not isinstance(dados_prova, dict):
        print("Informe um dicionário com os dados da prova.")
        return None
    for campo in ("serie", "disciplina", "bimestre", "modelo_padrao"):
        valor = dados_prova.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            print("Campo obrigatório inválido:", campo)
            return None
    questoes = dados_prova.get("questoes")
    if not isinstance(questoes, list) or not 1 <= len(questoes) <= _limite_questoes():
        print("Quantidade de questões fora do limite da escola.")
        return None
    if not all(questao_valida(questao) for questao in questoes):
        print("Revise os campos, alternativas e gabaritos das questões.")
        return None
    try:
        padroes.obter_modelo(dados_prova["modelo_padrao"])
    except ValueError as erro:
        print(erro)
        return None
    referencias = _referencias_permitidas(dados_prova, autor)
    if not referencias:
        return None
    if not hasattr(biblioteca, "registrar_uso"):
        print("A gravação da prova requer o registro de uso da biblioteca do contrato v1.")
        return None
    registros = _ler_atividades()
    if registros is None:
        return None
    novo_id = max((atividade["id"] for atividade in registros), default=0) + 1
    nova = {
        "id": novo_id, "professor_id": professor_id,
        "serie": dados_prova["serie"], "disciplina": dados_prova["disciplina"],
        "bimestre": dados_prova["bimestre"], "materiais_referenciados": referencias,
        "questoes": questoes, "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "modelo_padrao": dados_prova["modelo_padrao"],
    }
    if not _gravar_atividades(registros, registros + [nova]):
        return None
    print("Prova salva com ID", novo_id)
    for numero in referencias:
        try:
            if biblioteca.registrar_uso(numero) is False:
                print(f"Prova {novo_id} salva. Uso do material {numero} não registrado.")
        except (OSError, ValueError) as erro:
            print(f"Prova {novo_id} salva. Falha ao contar uso do material {numero}:", erro)
    return nova


def gerar_prova(usuario):
    autor = _usuario_ativo(usuario)
    if not autor:
        return None
    disponiveis = _materiais_aprovados(autor)
    if not disponiveis:
        print("Nenhum material aprovado disponível para gerar uma prova.")
        return None
    limite = _limite_questoes()
    if not limite:
        return None
    for material in disponiveis:
        print(f"[{material['id']}] {material['titulo']} | {material['serie']} | {material['disciplina']}")
    numero = ler_numero("ID do material (0 para voltar): ")
    if numero == 0:
        return None
    for material in disponiveis:
        if material["id"] == numero:
            break
    else:
        print("Material indisponível.")
        return None
    print("1 - Múltipla escolha   2 - Discursiva   3 - Verdadeiro ou falso")
    tipo = ler_numero("Tipo de questão: ")
    print("1 - Fácil   2 - Média   3 - Difícil")
    nivel = ler_numero("Dificuldade: ")
    if tipo not in (1, 2, 3) or nivel not in (1, 2, 3):
        print("Tipo ou dificuldade inválidos.")
        return None
    questoes = questoes_do_material(material, TIPOS[tipo - 1], DIFICULDADES[nivel - 1])
    disponivel = min(limite, len(questoes))
    print(f"O texto permite {len(questoes)} questão(ões) distinta(s) desse tipo. Limite da escola: {limite}.")
    if not disponivel:
        return None
    while True:
        quantidade = ler_numero(f"Quantidade (1 a {disponivel}, 0 para voltar): ")
        if quantidade == 0:
            return None
        if quantidade is not None and 1 <= quantidade <= disponivel:
            break
        print(f"Escolha no máximo {disponivel} questão(ões) para este material.")
    rascunho = {
        "serie": material["serie"], "disciplina": material["disciplina"], "bimestre": material["bimestre"],
        "materiais_referenciados": [material["id"]], "questoes": questoes[:quantidade],
        "modelo_padrao": "institucional_v1",
    }
    revisada = editar_prova_gerada(rascunho)
    if revisada:
        return salvar_prova(autor["id"], revisada, usuario=autor)
    print("Rascunho descartado.")
    return None


def gerar_atividade(usuario=None):
    """Entrada mantida para o menu anterior."""
    return gerar_prova(usuario)


def _ordem_criacao(atividade):
    try:
        data = datetime.strptime(atividade["data_criacao"], "%d/%m/%Y %H:%M")
    except (KeyError, ValueError, TypeError):
        data = datetime.min
    return data, atividade["id"]


def listar_historico(professor_id=None, usuario=None):
    atual = _usuario_ativo(usuario)
    if not atual:
        return []
    if atual["perfil"] != "coordenacao":
        if professor_id is not None and atual["id"] != professor_id:
            print("Você só pode consultar o próprio histórico.")
            return []
        professor_id = atual["id"]
    registros = _ler_atividades()
    if registros is None:
        return []
    historico = [a for a in registros if professor_id is None or verificar_autoria(a, professor_id)]
    historico.sort(key=_ordem_criacao, reverse=True)
    for atividade in historico:
        print(f"[{atividade['id']}] {atividade.get('data_criacao', '')} | Autor {atividade['professor_id']} | "
              f"{atividade.get('serie', '')} | {atividade.get('disciplina', '')} | {atividade.get('bimestre', '')}")
    if not historico:
        print("Nenhuma prova encontrada.")
    return historico


def editar_questao(professor_id, atividade_id, indice_questao, dados_questao, usuario=None, prova_anterior=None):
    atual = _usuario_ativo(usuario)
    if not atual:
        return False
    registros = _ler_atividades()
    prova = _atividade_permitida(registros, atividade_id, atual)
    if not prova or professor_id not in (atual["id"], prova["professor_id"]):
        return False
    if prova_anterior is not None and prova != prova_anterior:
        print("A prova mudou durante a revisão. Abra a edição novamente.")
        return False
    if type(indice_questao) is not int or not 0 <= indice_questao < len(prova["questoes"]):
        print("Índice de questão inválido.")
        return False
    if not questao_valida(dados_questao):
        print("Questão inválida. Confira os campos, as alternativas e o gabarito.")
        return False
    questoes = prova["questoes"].copy()
    questoes[indice_questao] = dados_questao
    novas = registros.copy()
    novas[registros.index(prova)] = dict(prova, questoes=questoes)
    if _gravar_atividades(registros, novas):
        print("Questão editada.")
        return True
    return False


def excluir_prova(atividade_id, professor_id, usuario=None):
    atual = _usuario_ativo(usuario)
    if not atual:
        return False
    registros = _ler_atividades()
    prova = _atividade_permitida(registros, atividade_id, atual)
    if not prova or professor_id not in (atual["id"], prova["professor_id"]):
        return False
    if input(f"Excluir a prova {atividade_id}? (s/n): ").strip().lower() != "s":
        print("Exclusão cancelada.")
        return False
    atual = _usuario_ativo(usuario)
    if not _atividade_permitida(registros, atividade_id, atual):
        return False
    novas = registros.copy()
    novas.remove(prova)
    if _gravar_atividades(registros, novas):
        print("Prova excluída.")
        return True
    return False


def exportar_prova(atividade_id, usuario):
    atual = _usuario_ativo(usuario)
    if not atual:
        return []
    prova = _atividade_permitida(_ler_atividades(), atividade_id, atual)
    if not prova:
        return []
    if not hasattr(padroes, "exportar_prova_formatada"):
        print("A exportação requer o módulo de padrões do contrato v1.")
        return []
    try:
        return padroes.exportar_prova_formatada(prova)
    except (OSError, TypeError, ValueError) as erro:
        print("Não foi possível exportar a prova:", erro)
        return []


def _editar_no_menu(atividade_id, usuario):
    prova = _atividade_permitida(_ler_atividades(), atividade_id, _usuario_ativo(usuario))
    if not prova:
        return
    for numero, questao in enumerate(prova["questoes"], 1):
        mostrar_questao(numero, questao)
    numero = ler_numero("Número da questão a editar: ")
    if numero is None or not 1 <= numero <= len(prova["questoes"]):
        print("Número de questão inválido.")
        return
    edicao = revisar_questao(prova["questoes"][numero - 1])
    if edicao:
        editar_questao(usuario["id"], atividade_id, numero - 1, edicao, usuario=usuario, prova_anterior=prova)


def gerenciar_provas(usuario):
    while _usuario_ativo(usuario):
        print("\n1 - Gerar prova   2 - Histórico   3 - Editar questão   4 - Excluir   5 - Exportar   0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if opcao == "1":
            gerar_prova(usuario)
        elif opcao == "2":
            listar_historico(usuario=usuario)
        elif opcao in ("3", "4", "5"):
            atividade_id = ler_numero("ID da prova: ")
            if atividade_id is None:
                continue
            if opcao == "3":
                _editar_no_menu(atividade_id, usuario)
            elif opcao == "4":
                excluir_prova(atividade_id, usuario["id"], usuario=usuario)
            else:
                for caminho in exportar_prova(atividade_id, usuario):
                    print("Arquivo:", caminho)
        else:
            print("Opção inválida.")
