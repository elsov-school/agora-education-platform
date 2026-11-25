"""Testes do módulo de usuários com um cadastro temporário por caso."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from usuarios import usuarios as cadastro


def dados_iniciais():
    return [
        {"id": 1, "nome": "Coordenação de teste", "email": "coord@example.test",
         "perfil": "coordenacao", "ativo": True, "turmas_lecionadas": []},
        {"id": 4, "nome": "Docente de teste", "email": "docente@example.test",
         "perfil": "professor", "ativo": True, "turmas_lecionadas": ["6A_CIEN", "7B_CIEN", "X"]},
        {"id": 7, "nome": "Docente inativo", "email": "inativo@example.test",
         "perfil": "professor", "ativo": False, "turmas_lecionadas": ["8A_MAT", "9A_MAT"]},
    ]


def verificar_migracao(arquivo, coord):
    """Os códigos conhecidos geram as quatro atribuições e a leitura preserva o arquivo."""
    original = arquivo.read_bytes()
    usuarios = cadastro.carregar_usuarios()
    assert usuarios[0]["atribuicoes"] == []
    assert usuarios[1]["atribuicoes"] == [
        {"turma": "6A", "serie": "6º ano", "disciplina": "Ciências"},
        {"turma": "7B", "serie": "7º ano", "disciplina": "Ciências"},
    ]
    assert usuarios[2]["atribuicoes"] == [
        {"turma": "8A", "serie": "8º ano", "disciplina": "Matemática"},
        {"turma": "9A", "serie": "9º ano", "disciplina": "Matemática"},
    ]
    assert usuarios[1]["turmas_lecionadas"] == ["6A_CIEN", "7B_CIEN", "X"]
    assert arquivo.read_bytes() == original


def verificar_login(arquivo, coord):
    """O login exige e-mail e senha, rejeita IDs e inativos e permite sair."""
    registros = cadastro.carregar_usuarios()
    for registro in registros:
        registro.update(cadastro.preparar_senha("SenhaTeste123!"))
    arquivo.write_text(json.dumps(registros), encoding="utf-8")
    with patch("builtins.input", side_effect=["inativo@example.test", "4", "  DOCENTE@example.test "]), \
            patch.object(cadastro, "ler_senha", return_value="SenhaTeste123!"):
        assert cadastro.fazer_login()["id"] == 4
    with patch("builtins.input", return_value="coord@example.test"), \
            patch.object(cadastro, "ler_senha", return_value="SenhaTeste123!"):
        assert cadastro.fazer_login()["id"] == 1
    with patch("builtins.input", return_value="0"):
        assert cadastro.fazer_login() is None


def verificar_menu(arquivo, coord):
    """A coordenação cadastra e atualiza atribuições pelo menu, que persistem após novo login."""
    coord = cadastro.configurar_primeiro_acesso("coord@example.test", "SenhaTeste123!")
    with patch.object(cadastro, "ler_senha", return_value="SenhaTeste123!"), patch("builtins.input", side_effect=[
        "1", "  Bia  ", " BIA@example.test ", "6A_CIEN, 8B | 8º ano | História, X",
        "2", "4", "8", "7A | 7º ano | Geografia", "3", "0",
    ]):
        cadastro.gerenciar_usuarios(coord)
    with patch("builtins.input", return_value="bia@example.test"), \
            patch.object(cadastro, "ler_senha", return_value="SenhaTeste123!"):
        docente = cadastro.fazer_login()
    assert docente["id"] == 8 and docente["nome"] == "Bia"
    assert docente["turmas_lecionadas"] == ["7A"]
    assert docente["atribuicoes"] == [{"turma": "7A", "serie": "7º ano", "disciplina": "Geografia"}]
    assert [p["id"] for p in cadastro.listar_professores(usuario=coord)] == [4, 8]
    assert [p["id"] for p in cadastro.listar_professores(True, coord)] == [4, 7, 8]


def verificar_filtro(arquivo, coord):
    """A permissão exige aprovação e correspondência em uma só atribuição."""
    atribuicoes = [
        {"turma": "6A", "serie": "6º ano", "disciplina": "Ciências"},
        {"turma": "7B", "serie": "7º ano", "disciplina": "História"},
    ]
    docente = cadastro.atualizar_turmas(4, ["6A", "7B"], coord, atribuicoes)
    geral = {"serie": " 6º Ano ", "disciplina": "CIÊNCIAS", "status_validacao": "aprovado_coordenacao"}
    materiais = [
        geral, dict(geral, turma="6a"), dict(geral, turma="6B"),
        dict(geral, turma="7B"), dict(geral, serie="7º ano"),
        dict(geral, disciplina="História"), dict(geral, status_validacao="pendente"),
        {"serie": "6º ano", "disciplina": "Ciências"},
        dict(geral, turma="7B", serie="7º ano", disciplina="História"),
        dict(geral, turma=12), dict(geral, serie=""), dict(geral, turma=" "),
    ]
    esperados = [materiais[n] for n in (0, 1, 8, 11)]
    assert cadastro.filtrar_materiais_do_professor(docente, materiais) == esperados
    assert cadastro.filtrar_materiais_do_professor(coord, materiais) == materiais
    for material in materiais:
        assert cadastro.usuario_pode_acessar_material(docente, material) == (material in esperados)

    cadastro.atualizar_turmas(4, ["6A_CIEN"], coord, atribuicoes=[])
    assert cadastro.filtrar_materiais_do_professor(docente, materiais) == []
    cadastro.atualizar_turmas(4, ["6A_DESCONHECIDO"], coord)
    assert not cadastro.usuario_pode_acessar_material(docente, geral)


def verificar_permissoes(arquivo, coord):
    """A chamada direta de gestão ou leitura de material exige permissão atual."""
    docente, inativo = cadastro.carregar_usuarios()[1:]
    assert cadastro.verificar_permissao(1, "gerenciar_usuarios")
    assert cadastro.verificar_permissao(4, "acessar_conteudos")
    assert not cadastro.verificar_permissao(4, "gerenciar_usuarios")
    assert not cadastro.verificar_permissao(7, "acessar_conteudos")
    assert not cadastro.verificar_permissao(99, "acessar_metricas")
    original = arquivo.read_bytes()
    for ator in (None, docente, inativo, dict(docente, perfil="coordenacao"), dict(coord, ativo=False)):
        for funcao, args in [
            (cadastro.cadastrar_professor, ("Docente", "novo@example.test", [])),
            (cadastro.atualizar_turmas, (4, [])), (cadastro.desativar_usuario, (4,)),
            (cadastro.listar_professores, ()), (cadastro.salvar_usuarios, ([],)),
        ]:
            with unittest.TestCase().assertRaises(PermissionError):
                funcao(*args, usuario=ator)
        with patch("builtins.input", side_effect=AssertionError("O menu foi aberto.")):
            cadastro.gerenciar_usuarios(ator)
    assert arquivo.read_bytes() == original
    assert not cadastro.usuario_pode_acessar_material(None, {})
    assert cadastro.filtrar_materiais_do_professor(inativo, [{}]) == []

    cadastro.desativar_usuario(4, coord)
    material = {"serie": "6º ano", "disciplina": "Ciências", "status_validacao": "aprovado_coordenacao"}
    assert not cadastro.usuario_pode_acessar_material(docente, material)
    atual = cadastro.buscar_usuario(cadastro.carregar_usuarios(), 4)
    assert atual["ativo"] is False and atual["atribuicoes"] == docente["atribuicoes"]
    assert not cadastro.verificar_permissao(4, "acessar_conteudos")
    with patch("builtins.input", side_effect=["4", "0"]):
        assert cadastro.fazer_login() is None


def verificar_entradas(arquivo, coord):
    """Entradas inválidas conservam os cadastros anteriores."""
    original = arquivo.read_bytes()
    for nome, email, turmas, atribuicoes in [
        ("", "novo@example.test", [], []), ("Bia", "sem-arroba", [], []),
        ("Bia", "a@@b", [], []), ("Bia", " DOCENTE@example.test ", [], []),
        ("Bia", "novo@example.test", "6A_CIEN", None),
        ("Bia", "novo@example.test", ["6A"], [{"turma": "6A", "serie": ""}]),
    ]:
        with unittest.TestCase().assertRaises(ValueError):
            cadastro.cadastrar_professor(nome, email, turmas, coord, atribuicoes)
    with unittest.TestCase().assertRaises(ValueError):
        cadastro.atualizar_turmas(1, [], coord)
    with unittest.TestCase().assertRaises(ValueError):
        cadastro.desativar_usuario(999, coord)
    with unittest.TestCase().assertRaises(ValueError):
        cadastro.desativar_usuario(7, coord)
    assert arquivo.read_bytes() == original


def verificar_arquivo_invalido(arquivo, coord):
    """JSON truncado, malformado ou com formato inválido é preservado."""
    invalidos = [b"[", b"{}", b"[{}]", b"\xff"]
    registro = dados_iniciais()[1]
    for atribuicoes in (None, [{"turma": "6A"}]):
        invalidos.append(json.dumps([dict(registro, atribuicoes=atribuicoes)]).encode())
    for conteudo in invalidos:
        arquivo.write_bytes(conteudo)
        with patch("builtins.input", return_value="1"):
            assert cadastro.fazer_login() is None
        with unittest.TestCase().assertRaises(ValueError):
            cadastro.cadastrar_professor("Bia", "bia@example.test", [], coord)
        with unittest.TestCase().assertRaises(ValueError):
            cadastro.salvar_usuarios([], coord)
        assert not cadastro.verificar_permissao(1, "gerenciar_usuarios")
        assert not cadastro.usuario_pode_acessar_material(coord, {})
        assert cadastro.filtrar_materiais_do_professor(coord, [{}]) == []
        assert arquivo.read_bytes() == conteudo


def verificar_gravacao(arquivo, coord):
    """Falha de substituição e atualização concorrente preservam o cadastro concluído."""
    original = arquivo.read_bytes()
    with patch.object(cadastro.os, "replace", side_effect=OSError("gravação interrompida")):
        with unittest.TestCase().assertRaises(OSError):
            cadastro.desativar_usuario(4, coord)
    assert arquivo.read_bytes() == original
    temporario = Path(str(arquivo) + ".tmp")
    assert not temporario.exists()

    anteriores = cadastro.carregar_usuarios()
    cadastro.cadastrar_professor("Bia", "bia@example.test", [], coord)
    atual = arquivo.read_bytes()
    with unittest.TestCase().assertRaisesRegex(ValueError, "cadastro mudou"):
        cadastro.salvar_usuarios(anteriores, coord, anteriores)
    assert arquivo.read_bytes() == atual and not temporario.exists()
    temporario.write_text("outra gravação", encoding="utf-8")
    with unittest.TestCase().assertRaisesRegex(ValueError, "em andamento"):
        cadastro.desativar_usuario(4, coord)
    assert arquivo.read_bytes() == atual and temporario.read_text(encoding="utf-8") == "outra gravação"


def caso_temporario(verificar):
    def executar():
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "usuarios.json"
            registros = dados_iniciais()
            arquivo.write_text(json.dumps(registros), encoding="utf-8")
            with patch.object(cadastro, "ARQUIVO_USUARIOS", str(arquivo)), patch("sys.stdout", new=io.StringIO()):
                verificar(arquivo, registros[0])
    return unittest.FunctionTestCase(executar, description=verificar.__doc__)


def load_tests(loader, suite, pattern):
    for verificar in (verificar_migracao, verificar_login, verificar_menu, verificar_filtro,
                      verificar_permissoes, verificar_entradas, verificar_arquivo_invalido, verificar_gravacao):
        suite.addTest(caso_temporario(verificar))
    return suite
