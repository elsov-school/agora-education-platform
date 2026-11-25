"""Cadastro de usuários, login acadêmico e acesso à biblioteca do Ágora."""

import json
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_USUARIOS = os.path.join(PASTA_ATUAL, "usuarios.json")

PERMISSOES = {
    "coordenacao": {"gerenciar_usuarios", "aprovar_materiais", "acessar_metricas"},
    "professor": {"acessar_conteudos", "gerenciar_atividades"},
}

TURMAS_DEMONSTRACAO = {
    "6A_CIEN": ("6A", "6º ano", "Ciências"),
    "7B_CIEN": ("7B", "7º ano", "Ciências"),
    "8A_MAT": ("8A", "8º ano", "Matemática"),
    "9A_MAT": ("9A", "9º ano", "Matemática"),
}


def normalizar_turmas(turmas_lecionadas):
    if not isinstance(turmas_lecionadas, list):
        raise ValueError("Informe uma lista de turmas.")
    turmas = []
    for turma in turmas_lecionadas:
        if not isinstance(turma, str):
            raise ValueError("O código da turma deve ser texto.")
        codigo = turma.strip().upper()
        if codigo and codigo not in turmas:
            turmas.append(codigo)
    return turmas


def preparar_atribuicoes(turmas, atribuicoes):
    """Uma lista explícita, inclusive vazia, substitui o mapa de demonstração."""
    if atribuicoes is None:
        atribuicoes = []
        for codigo in turmas:
            if codigo in TURMAS_DEMONSTRACAO:
                turma, serie, disciplina = TURMAS_DEMONSTRACAO[codigo]
                atribuicoes.append({"turma": turma, "serie": serie, "disciplina": disciplina})

    if not isinstance(atribuicoes, list):
        raise ValueError("Informe uma lista de atribuições.")
    resultado = []
    for item in atribuicoes:
        if not isinstance(item, dict):
            raise ValueError("Cada atribuição precisa de turma, série e disciplina.")
        atribuicao = {}
        for campo in ("turma", "serie", "disciplina"):
            valor = item.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError("Preencha turma, série e disciplina em cada atribuição.")
            atribuicao[campo] = valor.strip()
        atribuicao["turma"] = atribuicao["turma"].upper()
        if atribuicao not in resultado:
            resultado.append(atribuicao)
    return resultado


def validar_cadastro(usuarios):
    """Recusa dados inválidos antes de operar sobre o cadastro."""
    if not isinstance(usuarios, list):
        raise ValueError("O cadastro deve conter uma lista de usuários.")
    ids = set()
    emails = set()
    for registro in usuarios:
        if not isinstance(registro, dict):
            raise ValueError("Registro de usuário inválido.")
        numero = registro.get("id")
        if type(numero) is not int or numero < 1 or numero in ids:
            raise ValueError("ID inválido ou repetido no cadastro.")
        ids.add(numero)
        for campo in ("nome", "email", "perfil"):
            if not isinstance(registro.get(campo), str) or not registro[campo].strip():
                raise ValueError(f"Campo {campo} inválido no cadastro.")
        email = registro["email"].strip().casefold()
        if email in emails:
            raise ValueError("E-mail repetido no cadastro.")
        emails.add(email)
        if registro["perfil"] not in PERMISSOES or type(registro.get("ativo")) is not bool:
            raise ValueError("Perfil ou situação inválida no cadastro.")
        turmas = normalizar_turmas(registro.get("turmas_lecionadas"))
        if "atribuicoes" in registro and not isinstance(registro["atribuicoes"], list):
            raise ValueError("O campo atribuicoes deve ser uma lista.")
        atribuicoes = preparar_atribuicoes(turmas, registro.get("atribuicoes"))
        if "atribuicoes" not in registro:
            registro["atribuicoes"] = atribuicoes


def carregar_usuarios():
    """Lê o JSON. A leitura de cadastros antigos não altera o arquivo."""
    try:
        with open(ARQUIVO_USUARIOS, encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise ValueError("Não foi possível ler usuarios.json. Verifique o cadastro.") from erro
    validar_cadastro(usuarios)
    return usuarios


def gerar_novo_id(usuarios):
    if not usuarios:
        return 1
    return max(usuario["id"] for usuario in usuarios) + 1


def buscar_usuario(usuarios, usuario_id):
    if type(usuario_id) is int:
        for usuario in usuarios:
            if usuario["id"] == usuario_id:
                return usuario
    return None


def usuario_da_sessao(usuario, usuarios):
    """Revalida a sessão e usa as atribuições e a situação atuais do cadastro."""
    if not isinstance(usuario, dict) or usuario.get("ativo") is not True:
        return None
    atual = buscar_usuario(usuarios, usuario.get("id"))
    if atual and atual["ativo"] and atual["perfil"] == usuario.get("perfil"):
        return atual
    return None


def exigir_coordenacao(usuario, usuarios):
    atual = usuario_da_sessao(usuario, usuarios)
    if atual is None or atual["perfil"] != "coordenacao":
        raise PermissionError("A gestão de usuários exige uma coordenação ativa.")


def salvar_usuarios(usuarios, usuario=None, anteriores=None):
    """Só substitui o JSON depois de gravar o cadastro completo ao lado dele."""
    temporario = f"{ARQUIVO_USUARIOS}.tmp"
    try:
        arquivo = open(temporario, "x", encoding="utf-8")
    except FileExistsError as erro:
        raise ValueError("Há uma gravação de usuários em andamento. Tente novamente.") from erro
    gravado = False
    try:
        with arquivo:
            atuais = carregar_usuarios()
            exigir_coordenacao(usuario, atuais)
            if anteriores is not None and atuais != anteriores:
                raise ValueError("O cadastro mudou. Consulte os dados e repita a operação.")
            validar_cadastro(usuarios)
            json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        os.replace(temporario, ARQUIVO_USUARIOS)
        gravado = True
    finally:
        if not gravado:
            os.remove(temporario)


def cadastrar_professor(nome, email, turmas_lecionadas, usuario=None, atribuicoes=None):
    usuarios = carregar_usuarios()
    exigir_coordenacao(usuario, usuarios)
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome não pode ficar vazio.")
    if not isinstance(email, str):
        raise ValueError("Informe um e-mail válido.")
    email = email.strip().lower()
    partes = email.split("@")
    if len(partes) != 2 or not all(partes) or len(email.split()) != 1:
        raise ValueError("Informe um e-mail válido.")
    for registro in usuarios:
        if registro["email"].strip().casefold() == email.casefold():
            raise ValueError("Já existe um usuário com esse e-mail.")

    turmas = normalizar_turmas(turmas_lecionadas)
    professor = {
        "id": gerar_novo_id(usuarios),
        "nome": nome.strip(),
        "email": email,
        "perfil": "professor",
        "turmas_lecionadas": turmas,
        "atribuicoes": preparar_atribuicoes(turmas, atribuicoes),
        "ativo": True,
    }
    salvar_usuarios(usuarios + [professor], usuario, usuarios)
    return professor


def listar_professores(incluir_inativos=False, usuario=None):
    usuarios = carregar_usuarios()
    exigir_coordenacao(usuario, usuarios)
    professores = []
    for registro in usuarios:
        if registro["perfil"] == "professor" and (registro["ativo"] or incluir_inativos):
            professores.append(registro)
    return professores


def atualizar_turmas(usuario_id, turmas_lecionadas, usuario=None, atribuicoes=None):
    usuarios = carregar_usuarios()
    exigir_coordenacao(usuario, usuarios)
    professor = buscar_usuario(usuarios, usuario_id)
    if professor is None or professor["perfil"] != "professor":
        raise ValueError("Informe o ID de um professor cadastrado.")
    turmas = normalizar_turmas(turmas_lecionadas)
    novos = usuarios.copy()
    atualizado = professor.copy()
    atualizado["turmas_lecionadas"] = turmas
    atualizado["atribuicoes"] = preparar_atribuicoes(turmas, atribuicoes)
    novos[usuarios.index(professor)] = atualizado
    salvar_usuarios(novos, usuario, usuarios)
    return atualizado


def desativar_usuario(usuario_id, usuario=None):
    usuarios = carregar_usuarios()
    exigir_coordenacao(usuario, usuarios)
    alvo = buscar_usuario(usuarios, usuario_id)
    if alvo is None:
        raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")
    if not alvo["ativo"]:
        raise ValueError("Esse usuário já está inativo.")
    novos = usuarios.copy()
    inativo = alvo.copy()
    inativo["ativo"] = False
    novos[usuarios.index(alvo)] = inativo
    salvar_usuarios(novos, usuario, usuarios)
    return inativo


def _usuarios_para_acesso():
    try:
        return carregar_usuarios()
    except (ValueError, OSError) as erro:
        print(f"Erro ao verificar o acesso: {erro}")
        return []


def verificar_permissao(usuario_id, acao):
    usuario = buscar_usuario(_usuarios_para_acesso(), usuario_id)
    return bool(usuario and usuario["ativo"] and acao in PERMISSOES[usuario["perfil"]])


def _material_permitido(usuario, material):
    if usuario is None or not isinstance(material, dict):
        return False
    if usuario["perfil"] == "coordenacao":
        return True
    if material.get("status_validacao") != "aprovado_coordenacao":
        return False
    turma = material.get("turma")
    if turma is None:
        turma = ""
    if not isinstance(turma, str):
        return False
    turma = turma.strip().casefold()
    serie = material.get("serie")
    disciplina = material.get("disciplina")
    if not isinstance(serie, str) or not isinstance(disciplina, str):
        return False
    for atribuicao in usuario["atribuicoes"]:
        if turma and turma != atribuicao["turma"].strip().casefold():
            continue
        if (serie.strip().casefold() == atribuicao["serie"].strip().casefold()
                and disciplina.strip().casefold() == atribuicao["disciplina"].strip().casefold()):
            return True
    return False


def usuario_pode_acessar_material(usuario, material):
    atual = usuario_da_sessao(usuario, _usuarios_para_acesso())
    return _material_permitido(atual, material)


def filtrar_materiais_do_professor(usuario, lista_materiais):
    atual = usuario_da_sessao(usuario, _usuarios_para_acesso())
    permitidos = []
    for material in lista_materiais:
        if _material_permitido(atual, material):
            permitidos.append(material)
    return permitidos


def fazer_login():
    """Identifica o usuário por ID ou e-mail no protótipo de terminal."""
    while True:
        entrada = input("ID ou e-mail (0 para sair): ").strip()
        if entrada == "0":
            return None
        try:
            usuarios = carregar_usuarios()
        except (ValueError, OSError) as erro:
            print(f"Erro ao abrir o cadastro: {erro}")
            return None
        for usuario in usuarios:
            if entrada == str(usuario["id"]) or entrada.casefold() == usuario["email"].strip().casefold():
                if usuario["ativo"]:
                    return usuario
                break
        print("Usuário não encontrado ou inativo.")


def ler_turmas():
    texto = input("Turmas (ex.: 6A_CIEN, 7B | 7º ano | História): ")
    return texto.split(",")


def ler_turmas_e_atribuicoes():
    """Aceita códigos antigos e atribuições completas na mesma entrada."""
    turmas = []
    atribuicoes = []
    for item in ler_turmas():
        if not item.strip():
            continue
        campos = item.split("|")
        turma = campos[0].strip().upper()
        if len(campos) == 3:
            atribuicoes.append({"turma": turma, "serie": campos[1], "disciplina": campos[2]})
        elif len(campos) == 1:
            atribuicoes.extend(preparar_atribuicoes([turma], None))
            if turma not in TURMAS_DEMONSTRACAO:
                print(f"Código {turma} sem atribuição. Informe turma | série | disciplina para dar acesso.")
        else:
            raise ValueError("Use o formato turma | série | disciplina.")
        turmas.append(turma)
    return turmas, atribuicoes


def ler_id(pergunta):
    valor = input(pergunta).strip()
    if not valor.isdecimal():
        raise ValueError("O ID deve ser um número inteiro (ex.: 3).")
    return int(valor)


def mostrar_professores(professores):
    if not professores:
        print("Nenhum professor encontrado.")
    for professor in professores:
        situacao = "Ativo" if professor["ativo"] else "Inativo"
        turmas = ", ".join(professor["turmas_lecionadas"]) or "-"
        print(f"[{professor['id']}] {professor['nome']} | {professor['email']} | Turmas: {turmas} | {situacao}")
        for item in professor["atribuicoes"]:
            print(f"  {item['turma']} | {item['serie']} | {item['disciplina']}")
        if not professor["atribuicoes"]:
            print("  Sem atribuições. Use a opção 4 para completar o cadastro.")


def gerenciar_usuarios(usuario=None):
    while True:
        try:
            exigir_coordenacao(usuario, carregar_usuarios())
        except (ValueError, OSError) as erro:
            print(erro)
            return
        print("\n=== Gestão de Usuários ===")
        print("1 - Cadastrar professor")
        print("2 - Listar professores ativos")
        print("3 - Listar todos (inclui inativos)")
        print("4 - Atualizar turmas e atribuições de um professor")
        print("5 - Desativar usuário")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "1":
                nome = input("Nome: ")
                email = input("E-mail: ")
                turmas, atribuicoes = ler_turmas_e_atribuicoes()
                professor = cadastrar_professor(nome, email, turmas, usuario, atribuicoes)
                print(f"Professor '{professor['nome']}' cadastrado com ID {professor['id']}.")
            elif opcao in ("2", "3"):
                mostrar_professores(listar_professores(opcao == "3", usuario))
            elif opcao == "4":
                usuario_id = ler_id("ID do professor: ")
                turmas, atribuicoes = ler_turmas_e_atribuicoes()
                professor = atualizar_turmas(usuario_id, turmas, usuario, atribuicoes)
                print(f"Turmas de '{professor['nome']}' atualizadas.")
            elif opcao == "5":
                usuario_id = ler_id("ID do usuário: ")
                inativo = desativar_usuario(usuario_id, usuario)
                print(f"Usuário '{inativo['nome']}' desativado.")
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    sessao = fazer_login()
    if sessao:
        gerenciar_usuarios(sessao)
