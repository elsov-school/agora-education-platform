import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from painel import painel


class TestPainel(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.pasta = Path(pasta.name)
        self.biblioteca = self.pasta / "materiais.json"
        self.atividades = self.pasta / "atividades.json"
        self.cadastro = self.pasta / "usuarios.json"
        self.coord = {"id": 1, "perfil": "coordenacao", "ativo": True,
                      "nome": "Coordenação", "email": "coord@example.org",
                      "turmas_lecionadas": [], "atribuicoes": []}
        self.gravar(self.cadastro, [self.coord])
        self.gravar(self.atividades, [])
        self.gravar(self.biblioteca, [])
        for modulo, atributo, caminho in (
            (painel, "ARQUIVO_ATIVIDADES", self.atividades),
            (painel.biblioteca, "ARQUIVO_DADOS", self.biblioteca),
            (painel.cadastro, "ARQUIVO_USUARIOS", self.cadastro)
        ):
            self.enterContext(patch.object(modulo, atributo, str(caminho)))

    def gravar(self, caminho, registros):
        caminho.write_text(json.dumps(registros, ensure_ascii=False), encoding="utf-8")

    def abrir_painel(self, respostas, usuario=None):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=respostas), redirect_stdout(saida):
            painel.menu_painel(usuario)
        return saida.getvalue()

    def test_grupos_e_citacoes_historicas(self):
        atividades = [
            {"professor_id": 7, "disciplina": "Ciências", "serie": "6º ano",
             "materiais_referenciados": [20, 20]},
            {"professor_id": 8, "disciplina": "Ciências", "serie": "7º ano",
             "materiais_referenciados": [20, 8]}
        ]
        self.assertEqual(painel.contar_atividades_por_professor(atividades), {7: 1, 8: 1})
        self.assertEqual(painel.contar_atividades_por_disciplina(atividades), {"Ciências": 2})
        self.assertEqual(painel.contar_atividades_por_serie(atividades), {"6º ano": 1, "7º ano": 1})
        self.assertEqual(painel.listar_materiais_mais_citados(atividades, [{"id": 20, "titulo": "Luz"}]),
                         [(20, "Luz", 2), (8, "(material removido da biblioteca)", 1)])

    def test_top_tres_por_usos_com_desempate(self):
        materiais = [{"id": 10, "titulo": "B", "usos": 5}, {"id": 7, "titulo": "A", "usos": 5},
                     {"id": 3, "titulo": "D", "usos": 8}, {"id": 1, "titulo": "E", "usos": 1},
                     {"id": 9, "titulo": "Antigo"}]
        self.assertEqual(painel.listar_materiais_mais_usados(materiais),
                         [(3, "D", 8), (7, "A", 5), (10, "B", 5)])
        self.assertEqual(painel.listar_materiais_mais_usados([materiais[-1]]), [])

    def test_completo_somente_leitura_e_fila_legada(self):
        base = {"disciplina": "Ciências", "serie": "6º ano"}
        materiais = [dict(base, id=8, titulo="Mar", status_validacao="aprovado_coordenacao", usos=4),
                     dict(base, id=2, titulo="Solo"), dict(base, id=1, titulo="Rocha", status_validacao="pendente")]
        self.gravar(self.biblioteca, materiais)
        self.gravar(self.atividades, [dict(base, id=4, professor_id=3, materiais_referenciados=[8, 8])])
        arquivos = [self.biblioteca, self.atividades, self.cadastro]
        antes = [arquivo.read_bytes() for arquivo in arquivos]
        saida = self.abrir_painel(["5", "0"], self.coord)
        for trecho in ("Aprovados: 1", "Pendentes: 2", "[8] Mar - usos: 4",
                       "ID 3 (não cadastrado)", "ATIVIDADES GERADAS POR SÉRIE"):
            self.assertIn(trecho, saida)
        self.assertLess(saida.index("[1] Rocha"), saida.index("[2] Solo"))
        self.assertEqual(antes, [arquivo.read_bytes() for arquivo in arquivos])

    def test_rele_biblioteca_entre_escolhas(self):
        def respostas():
            yield "8"
            self.gravar(self.biblioteca, [{"id": 9, "titulo": "Célula", "usos": 2}])
            yield "8"
            yield "0"

        saida = self.abrir_painel(respostas(), self.coord)
        self.assertIn("Nenhum uso registrado", saida)
        self.assertIn("Célula - usos: 2", saida)

    def test_json_corrompido_preservado_e_erro_visivel(self):
        self.atividades.write_bytes(b"{")
        saida = self.abrir_painel(["5", "0"], self.coord)
        self.assertIn("Não foi possível calcular", saida)
        self.assertNotIn("Atividades geradas: 0", saida)
        self.assertEqual(self.atividades.read_bytes(), b"{")

    def test_permissao_e_id_isolado(self):
        self.assertIn("PAINEL DA COORDENAÇÃO", self.abrir_painel(["1", "0"]))
        self.assertIn("número inteiro", self.abrir_painel(["letra"]))
        self.assertIn("Acesso negado", self.abrir_painel([], dict(self.coord, perfil="professor")))
        self.gravar(self.cadastro, [dict(self.coord, ativo=False)])
        self.assertIn("Acesso negado", self.abrir_painel([], self.coord))
