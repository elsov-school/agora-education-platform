"""Testes procedurais de consultas com arquivos temporários."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from consultas import consultas
from materiais import materiais as biblioteca
from usuarios import usuarios


PROFESSOR = {"id": 9, "perfil": "professor", "ativo": True, "atribuicoes": [
    {"turma": "6A", "serie": "6º ano", "disciplina": "Ciências"},
]}
COORDENACAO = {"id": 1, "perfil": "coordenacao", "ativo": True}
LINHA = "  A Célula tem membrana.  "


def _materiais():
    base = {
        "id": 1, "titulo": "Caderno de ciências", "disciplina": "Ciências", "serie": "6º ano",
        "turma": "6A", "bimestre": "1º Bimestre", "tipo": "capitulo", "autor_upload": 9,
        "status_validacao": "aprovado_coordenacao", "usos": 2, "habilidade_bncc": "EF06CI05",
        "conteudo_texto": "Abertura do texto.\n" + LINHA + "\nOutra célula na mesma fonte.",
    }
    antigo = dict(base, id=2, titulo="Caderno antigo")
    antigo["bncc"] = antigo.pop("habilidade_bncc")
    antigo.pop("conteudo_texto")
    antigo["conteudo"] = "A célula aparece no microscópio."
    sem_status = dict(base, id=6, titulo="Sem validação")
    del sem_status["status_validacao"]
    return [
        base, antigo, dict(base, id=3, titulo="Em revisão", status_validacao="pendente"),
        dict(base, id=4, titulo="Outra turma", turma="6B"),
        dict(base, id=5, titulo="Outra disciplina", disciplina="Matemática"), sem_status,
    ]


def _executar(funcao, usuario, respostas, ids_permitidos, texto_json=None, falhar_uso=False):
    def filtrar(recebido, materiais):
        assert recebido is usuario
        return [m for m in materiais if m["id"] in ids_permitidos]

    if texto_json is None:
        texto_json = json.dumps(_materiais(), ensure_ascii=False)
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "materiais.json"
        caminho.write_text(texto_json, encoding="utf-8")
        saida = io.StringIO()
        with (
            patch.object(biblioteca, "ARQUIVO_DADOS", str(caminho)),
            patch.object(biblioteca, "materiais", []),
            patch.object(usuarios, "filtrar_materiais_do_professor", side_effect=filtrar,
                         create=True) as filtro,
            patch.object(biblioteca, "registrar_uso", return_value=True, create=True) as registrar,
            patch("builtins.input", side_effect=respostas),
            redirect_stdout(saida),
        ):
            if falhar_uso:
                registrar.side_effect = OSError("Falha de gravação")
            funcao(usuario)
        return (saida.getvalue(), [chamada.args[0] for chamada in registrar.call_args_list],
                filtro.call_count, caminho.read_text(encoding="utf-8"))


def test_consulta_literal_e_contagem():
    saida, registrados, filtragens, _ = _executar(
        consultas.consultar_com_evidencia, PROFESSOR, ["  ", " cÉlULA "], [1, 2],
    )
    assert filtragens == 1
    assert registrados == [1, 2]
    for esperado in ("Fonte: [1] Caderno de ciências", "Fonte: [2] Caderno antigo",
                     "Disciplina: Ciências", "Série: 6º ano", "Habilidade BNCC: EF06CI05",
                     "\n" + LINHA + "\n", "A célula aparece no microscópio."):
        assert esperado in saida, esperado
    for ausente in ("Outra turma", "Outra disciplina", "Abertura do texto", "Outra célula"):
        assert ausente not in saida, ausente


def test_coordenacao_consulta_somente_aprovados():
    saida, registrados, _, _ = _executar(
        consultas.consultar_conteudo, COORDENACAO, ["célula"], [1, 2, 3, 4, 5, 6],
    )
    assert registrados == [1, 2, 4, 5]
    assert "Em revisão" not in saida and "Sem validação" not in saida


def test_pesquisa_em_cinco_campos_sem_registrar_uso():
    for termo in ("Caderno", "Ciências", "6º ano", "membrana", "ef06ci05"):
        saida, registrados, _, _ = _executar(
            consultas.pesquisar_material, PROFESSOR, [termo], [1, 2, 3, 6],
        )
        assert "[1] Caderno de ciências" in saida, termo
        assert "Em revisão" not in saida and "Sem validação" not in saida
        assert "Outra turma" not in saida and "Outra disciplina" not in saida
        assert registrados == []


def test_titulo_sem_trecho_e_ausencia_de_permissao():
    for termo, permitidos in (("Caderno", [1, 2]), ("célula", [])):
        saida, registrados, _, _ = _executar(
            consultas.consultar_com_evidencia, PROFESSOR, [termo], permitidos,
        )
        assert "Nenhum trecho encontrado na base aprovada" in saida
        assert "Fonte:" not in saida and registrados == []


def test_entradas_sem_sessao_ou_inativas():
    for funcao in (consultas.pesquisar_material, consultas.consultar_com_evidencia,
                   consultas.consultar_conteudo):
        for usuario in (None, dict(PROFESSOR, ativo=False)):
            saida, registrados, filtragens, _ = _executar(funcao, usuario, [], [1, 2])
            assert "usuário ativo" in saida
            assert "Caderno" not in saida and registrados == [] and filtragens == 0


def test_json_invalido_preservado():
    saida, registrados, filtragens, arquivo = _executar(
        consultas.consultar_com_evidencia, PROFESSOR, ["célula"], [1], texto_json="{",
    )
    assert "Não foi possível" in saida
    assert registrados == [] and filtragens == 0 and arquivo == "{"


def test_falha_no_registro_de_uso():
    saida, registrados, _, _ = _executar(
        consultas.consultar_conteudo, PROFESSOR, ["célula"], [1], falhar_uso=True,
    )
    assert registrados == [1] and LINHA in saida
    assert "Não foi possível registrar o uso" in saida


def load_tests(loader, tests, pattern):
    for teste in (test_consulta_literal_e_contagem, test_coordenacao_consulta_somente_aprovados,
                  test_pesquisa_em_cinco_campos_sem_registrar_uso,
                  test_titulo_sem_trecho_e_ausencia_de_permissao,
                  test_entradas_sem_sessao_ou_inativas, test_json_invalido_preservado,
                  test_falha_no_registro_de_uso):
        tests.addTest(unittest.FunctionTestCase(teste))
    return tests
