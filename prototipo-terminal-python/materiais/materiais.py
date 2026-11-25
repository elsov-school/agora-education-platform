import json
import os
import time

from usuarios import usuarios as cadastro


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
ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materiais.json")


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


TIPOS = ("apostila", "capitulo", "plano_aula")
PENDENTE = "pendente"
APROVADO = "aprovado_coordenacao"
ARQUIVO_ATIVIDADES = os.path.join(os.path.dirname(ARQUIVO_DADOS), "..", "provas", "atividades.json")

# Versão lida do JSON. Impede uma edição antiga de sobrescrever uma consulta recente.
_texto_lido = None


def _migrar(registros):
    if not isinstance(registros, list):
        raise ValueError("A biblioteca deve conter uma lista.")
    novos = []
    ids = set()
    for registro in registros:
        if not isinstance(registro, dict):
            raise ValueError("Registro de material inválido.")
        item = registro.copy()
        identificador = item.get("id")
        if type(identificador) is not int or identificador < 1 or identificador in ids:
            raise ValueError("ID de material inválido ou repetido.")
        ids.add(identificador)
        for antigo, novo in (("bncc", "habilidade_bncc"), ("conteudo", "conteudo_texto")):
            item.setdefault(novo, item.get(antigo))
            item.setdefault(antigo, item[novo])
            if item[novo] != item[antigo]:
                raise ValueError(f"Material {identificador}: valores conflitantes em {antigo} e {novo}.")
        for campo in ("titulo", "disciplina", "serie", "bimestre", "bncc", "conteudo"):
            if not isinstance(item.get(campo), str) or not item[campo].strip():
                raise ValueError(f"Material {identificador}: campo {campo} inválido.")
        item.setdefault("tipo", "capitulo")
        item.setdefault("autor_upload", None)
        item.setdefault("status_validacao", PENDENTE)
        item.setdefault("usos", 0)
        if item["tipo"] not in TIPOS or item["status_validacao"] not in (PENDENTE, APROVADO):
            raise ValueError(f"Material {identificador}: tipo ou status desconhecido.")
        if type(item["usos"]) is not int or item["usos"] < 0:
            raise ValueError(f"Material {identificador}: usos deve ser um inteiro não negativo.")
        if item.get("turma") is not None and not isinstance(item["turma"], str):
            raise ValueError(f"Material {identificador}: turma inválida.")
        novos.append(item)
    return novos


def _ler_arquivo():
    try:
        with open(ARQUIVO_DADOS, encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        return None


def _gravar(novos, esperado):
    global _texto_lido
    texto = json.dumps(novos, ensure_ascii=False, indent=4) + "\n"
    temporario = ARQUIVO_DADOS + ".tmp"
    # Só um terminal prepara a gravação por vez. O original só muda ao final.
    arquivo = open(temporario, "x", encoding="utf-8")
    try:
        with arquivo:
            if _ler_arquivo() != esperado:
                raise FileExistsError("A biblioteca mudou durante a operação.")
            arquivo.write(texto)
        os.replace(temporario, ARQUIVO_DADOS)
    except (OSError, ValueError):
        os.remove(temporario)
        raise
    materiais[:] = novos
    _texto_lido = texto


def carregar_dados():
    global _texto_lido
    try:
        texto = _ler_arquivo()
        registros = materiais_exemplo() if texto is None else json.loads(texto)
        novos = _migrar(registros)
        if texto is None or novos != registros:
            _gravar(novos, texto)
        else:
            materiais[:] = novos
            _texto_lido = texto
        return True
    except (OSError, ValueError) as erro:
        materiais.clear()
        _texto_lido = None
        print("Não foi possível carregar materiais.json:", erro)
        return False


def _salvar(novos, esperado, usuario=None):
    if usuario is not None and not _autorizado(usuario):
        return False
    try:
        _gravar(_migrar(novos), esperado)
        return True
    except FileExistsError:
        print("A biblioteca mudou ou está em uso. Repita a operação com os dados atuais.")
    except (OSError, ValueError) as erro:
        print("Não foi possível salvar materiais.json:", erro)
    return False


def salvar_dados():
    """Persiste a lista compartilhada lida por carregar_dados()."""
    return _salvar(materiais, _texto_lido)


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


def _autorizado(usuario, perfis=("professor", "coordenacao")):
    if (isinstance(usuario, dict) and usuario.get("ativo") is True
            and usuario.get("perfil") in perfis and type(usuario.get("id")) is int
            and usuario["id"] > 0):
        try:
            atual = cadastro.buscar_usuario(cadastro.carregar_usuarios(), usuario["id"])
            if atual and atual.get("ativo") is True and atual.get("perfil") == usuario["perfil"]:
                return True
        except (ValueError, OSError, TypeError, KeyError) as erro:
            print("Não foi possível verificar a sessão no cadastro:", erro)
    print("Acesso negado para esta operação.")
    return False


def _visiveis(usuario):
    if usuario["perfil"] == "coordenacao":
        return materiais
    # O filtro por atribuição é compartilhado com consultas e provas.
    if not hasattr(cadastro, "filtrar_materiais_do_professor"):
        print("O filtro de atribuições do módulo usuários está indisponível.")
        return []
    return cadastro.filtrar_materiais_do_professor(usuario, materiais)


def _selecionar(lista, pergunta="ID: "):
    try:
        identificador = int(input(pergunta))
    except ValueError:
        print("Digite um número válido.")
        return None
    for item in lista:
        if item["id"] == identificador:
            return item
    print("Material não encontrado.")
    return None


def buscar_material_por_id(pergunta="ID: ", usuario=None):
    if _autorizado(usuario) and carregar_dados():
        return _selecionar(_visiveis(usuario), pergunta)


def _ler_campos(atual):
    titulo = ler_texto("Título: ", atual.get("titulo", ""))
    disciplina = escolher_opcao("Disciplina:", DISCIPLINAS, atual.get("disciplina", ""))
    serie = ler_texto("Série: ", atual.get("serie", ""))
    bimestre = escolher_opcao("Bimestre:", BIMESTRES, atual.get("bimestre", ""))
    bncc = ler_texto("Habilidade BNCC: ", atual.get("bncc", ""))
    conteudo = ler_texto("Conteúdo/descrição: ", atual.get("conteudo", ""))
    tipo = escolher_opcao("Tipo:", TIPOS, atual.get("tipo", ""))
    turma = input("Turma (opcional, Enter mantém, - remove): ").strip()
    if not turma:
        turma = atual.get("turma", "")
    elif turma == "-":
        turma = ""
    return {
        "titulo": titulo, "disciplina": disciplina, "serie": serie, "bimestre": bimestre,
        "bncc": bncc, "habilidade_bncc": bncc, "conteudo": conteudo,
        "conteudo_texto": conteudo, "tipo": tipo, "turma": turma,
    }


def adicionar_material(usuario=None):
    if not _autorizado(usuario) or not carregar_dados():
        return False
    versao = _texto_lido
    material = _ler_campos({})
    maior_id = 0
    for item in materiais:
        maior_id = max(maior_id, item["id"])
    material["id"] = maior_id + 1
    material["autor_upload"] = usuario["id"]
    material["status_validacao"] = APROVADO if usuario["perfil"] == "coordenacao" else PENDENTE
    material["usos"] = 0
    if not _salvar(materiais + [material], versao, usuario):
        return False
    print(f"Material {material['id']} cadastrado. Situação: {material['status_validacao']}.")
    return True


def _listar(lista):
    if not lista:
        print("Nenhum material disponível.")
    for item in lista:
        print(f"[{item['id']}] {item['titulo']} | {item['disciplina']} | "
              f"{item['serie']} | {item['status_validacao']}")


def listar_materiais(usuario=None):
    if _autorizado(usuario) and carregar_dados():
        _listar(_visiveis(usuario))


def mostrar_material(material):
    print("\nID:", material["id"])
    print("Título:", material["titulo"])
    print("Disciplina:", material["disciplina"])
    print("Série:", material["serie"])
    print("Turma:", material.get("turma") or "Toda a série")
    print("Bimestre:", material["bimestre"])
    print("Habilidade BNCC:", material["bncc"])
    print("Conteúdo:", material["conteudo"])
    print("Tipo:", material["tipo"])
    print("Situação:", material["status_validacao"])
    print("Autor (ID):", material["autor_upload"] or "Desconhecido")
    print("Usos:", material["usos"])


def visualizar_material(usuario=None):
    material = buscar_material_por_id(usuario=usuario)
    if material is not None:
        mostrar_material(material)


def _atualizar(material, campos, versao, usuario):
    novos = materiais.copy()
    alterado = material.copy()
    alterado.update(campos)
    novos[novos.index(material)] = alterado
    return _salvar(novos, versao, usuario)


def editar_material(usuario=None):
    material = buscar_material_por_id(usuario=usuario)
    if material is None:
        return False
    versao = _texto_lido
    professor = usuario["perfil"] == "professor"
    if professor and material["autor_upload"] != usuario["id"]:
        print("O professor só pode editar materiais de sua autoria.")
        return False
    mostrar_material(material)
    print("Pressione Enter para manter o valor atual de cada campo.")
    campos = _ler_campos(material)
    if professor:
        campos["status_validacao"] = PENDENTE
    if not _atualizar(material, campos, versao, usuario):
        return False
    print("Material atualizado.")
    return True


def aprovar_materiais_pendentes(usuario):
    if not _autorizado(usuario, ("coordenacao",)) or not carregar_dados():
        return False
    versao = _texto_lido
    pendentes = [item for item in materiais if item["status_validacao"] == PENDENTE]
    if not pendentes:
        print("Nenhum material pendente.")
        return False
    _listar(pendentes)
    material = _selecionar(pendentes, "ID para revisar (0 para voltar): ")
    if material is None:
        return False
    mostrar_material(material)
    if input("Aprovar este material? (s/n) ").strip().lower() != "s":
        print("Aprovação cancelada.")
        return False
    if not _atualizar(material, {"status_validacao": APROVADO}, versao, usuario):
        return False
    print("Material aprovado pela coordenação.")
    return True


def _pode_excluir(material_id):
    try:
        with open(ARQUIVO_ATIVIDADES, encoding="utf-8") as arquivo:
            atividades = json.load(arquivo)
        if not isinstance(atividades, list):
            raise ValueError("O histórico deve conter uma lista.")
        for atividade in atividades:
            if not isinstance(atividade, dict) or not isinstance(atividade.get("materiais_referenciados"), list):
                raise ValueError("Atividade com referências inválidas.")
            for referencia in atividade["materiais_referenciados"]:
                if type(referencia) is not int or referencia < 1:
                    raise ValueError("ID de material inválido no histórico.")
                if referencia == material_id:
                    print("Exclusão bloqueada: uma prova referencia este material.")
                    return False
        return True
    except (OSError, ValueError) as erro:
        print("Exclusão bloqueada. Não foi possível verificar o histórico de provas:", erro)
        return False


def excluir_material(usuario=None):
    if not _autorizado(usuario, ("coordenacao",)) or not carregar_dados():
        return False
    versao = _texto_lido
    material = _selecionar(materiais)
    if material is None:
        return False
    mostrar_material(material)
    if input("Tem certeza que deseja excluir? (s/n) ").strip().lower() != "s":
        print("Exclusão cancelada.")
        return False
    if not _pode_excluir(material["id"]):
        return False
    novos = materiais.copy()
    novos.remove(material)
    if not _salvar(novos, versao, usuario):
        return False
    print("Material excluído.")
    return True


def registrar_uso(material_id):
    if type(material_id) is not int or material_id < 1:
        print("ID de material inválido.")
        return False
    for _ in range(8):
        try:
            versao = _ler_arquivo()
            if versao is None:
                print("Biblioteca não encontrada.")
                return False
            atuais = _migrar(json.loads(versao))
            for item in atuais:
                if item["id"] == material_id:
                    item["usos"] += 1
                    _gravar(atuais, versao)
                    return True
            print("Material não encontrado.")
            return False
        except FileExistsError:
            # Outro terminal pode ter contado um uso. Releia antes de tentar de novo.
            time.sleep(0.02)
        except (OSError, ValueError) as erro:
            print("Não foi possível registrar o uso:", erro)
            return False
    print("Biblioteca ocupada. Não foi possível registrar o uso.")
    return False


def gerenciar_materiais(usuario=None):
    while _autorizado(usuario) and carregar_dados():
        coordenacao = usuario["perfil"] == "coordenacao"
        print("\n=== Biblioteca curricular ===")
        _listar(_visiveis(usuario))
        print("1 - Visualizar material")
        print("2 - Editar material")
        if coordenacao:
            print("3 - Excluir material")
        print("4 - Cadastrar material" if coordenacao else "4 - Sugerir material")
        if coordenacao:
            print("5 - Aprovar material pendente")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            return
        if opcao == "1":
            visualizar_material(usuario)
        elif opcao == "2":
            editar_material(usuario)
        elif opcao == "3" and coordenacao:
            excluir_material(usuario)
        elif opcao == "4":
            adicionar_material(usuario)
        elif opcao == "5" and coordenacao:
            aprovar_materiais_pendentes(usuario)
        else:
            print("Opção inválida.")
