import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import call, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from provas import provas
from provas.geracao import TIPOS, questao_valida, questoes_do_material


class TestProvas(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.pasta = Path(pasta.name)
        self.atividades = self.pasta / "atividades.json"
        self.usuarios = self.pasta / "usuarios.json"
        self.materiais = self.pasta / "materiais.json"
        self.professor = {"id": 2, "perfil": "professor", "ativo": True}
        self.outro = {"id": 3, "perfil": "professor", "ativo": True}
        self.coord = {"id": 1, "perfil": "coordenacao", "ativo": True}
        for usuario in [self.coord, self.professor, self.outro]:
            usuario.update(nome=f"Pessoa {usuario['id']}", email=f"teste{usuario['id']}@example.org",
                           turmas_lecionadas=[], atribuicoes=[])
        self.professor["turmas_lecionadas"] = ["6A_CIEN"]
        self.professor["atribuicoes"] = [{"serie": "6º ano", "turma": "6A", "disciplina": "Ciências"}]
        self.gravar(self.usuarios, [self.coord, self.professor, self.outro])
        self.gravar(self.atividades, [])
        self.material = {
            "id": 10, "titulo": "Astronomia", "serie": "6º ano", "bimestre": "1º Bimestre",
            "disciplina": "Ciências", "status_validacao": "aprovado_coordenacao",
            "conteudo_texto": "A Terra gira. O Sol é uma estrela. A Terra gira.",
        }
        self.material.update(tipo="capitulo", autor_upload=1, usos=0, turma="6A",
                             conteudo=self.material["conteudo_texto"], bncc="EF06CI01", habilidade_bncc="EF06CI01")
        self.gravar(self.materiais, [
            self.material,
            dict(self.material, id=11, status_validacao="pendente", titulo="Pendente"),
            dict(self.material, id=12, titulo="Outra turma", turma="6B"),
            dict(self.material, id=13, titulo="Revisão"),
        ])
        self.trocar(provas, "ARQUIVO_DADOS", str(self.atividades))
        self.trocar(provas.usuarios, "ARQUIVO_USUARIOS", str(self.usuarios))
        self.trocar(provas.biblioteca, "ARQUIVO_DADOS", str(self.materiais))
        self.trocar(provas.biblioteca, "materiais", [])
        self.filtro = self.trocar(provas.usuarios, "filtrar_materiais_do_professor", side_effect=self.filtrar)
        self.regras = self.trocar(provas.padroes, "carregar_regras", return_value={"max_questoes": 2})
        self.uso = self.trocar(provas.biblioteca, "registrar_uso", return_value=True)
        self.exportar = self.trocar(provas.padroes, "exportar_prova_formatada", return_value=["aluno", "gabarito"])
        self.saida = io.StringIO()
        contexto = redirect_stdout(self.saida)
        contexto.__enter__()
        self.addCleanup(contexto.__exit__, None, None, None)
        self.questao = questoes_do_material(self.material, "discursiva", "facil")[0]
        self.dados = {
            "serie": "6º ano", "disciplina": "Ciências", "bimestre": "1º Bimestre",
            "questoes": [self.questao], "materiais_referenciados": [10], "modelo_padrao": "institucional_v1",
        }

    def trocar(self, modulo, nome, *args, **kwargs):
        substituto = patch.object(modulo, nome, *args, create=True, **kwargs)
        self.addCleanup(substituto.stop)
        return substituto.start()

    def gravar(self, arquivo, dados):
        arquivo.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    def registros(self):
        return json.loads(self.atividades.read_text(encoding="utf-8"))

    def filtrar(self, usuario, materiais):
        if usuario["perfil"] == "coordenacao":
            return materiais
        return [m for m in materiais if m["id"] in (10, 13) and usuario["id"] == 2]

    def salvar(self, **mudancas):
        return provas.salvar_prova(2, dict(self.dados, **mudancas), usuario=self.professor)

    def test_tres_tipos_distintos_ancorados_no_material(self):
        for tipo in TIPOS:
            with self.subTest(tipo=tipo):
                questoes = questoes_do_material(self.material, tipo, "media")
                self.assertEqual(questoes, questoes_do_material(self.material, tipo, "media"))
                self.assertEqual(len(questoes), 2)
                self.assertNotEqual(questoes[0]["enunciado"], questoes[1]["enunciado"])
                for questao in questoes:
                    self.assertTrue(questao_valida(questao))
                    self.assertEqual(questao["dificuldade"], "media")
                    self.assertIn("Astronomia", questao["enunciado"])
                if tipo == "discursiva":
                    self.assertEqual(questoes[0]["gabarito"], "A Terra gira.")
                    self.assertNotIn(questoes[0]["gabarito"], questoes[0]["enunciado"])
                elif tipo == "multipla_escolha":
                    self.assertEqual(questoes[0]["gabarito"], "gira")
                    self.assertEqual(set(questoes[0]["alternativas"]), {"A", "Terra", "gira"})
                else:
                    self.assertEqual([q["gabarito"] for q in questoes], ["Verdadeiro", "Falso"])
                    self.assertIn("estrela", questoes[1]["criterio_correcao"])

    def test_dificuldade_escolhida_altera_as_pistas_e_alternativas(self):
        material = dict(self.material, conteudo_texto="A Terra gira ao redor do Sol.")
        facil = questoes_do_material(material, "multipla_escolha", "facil")[0]
        dificil = questoes_do_material(material, "multipla_escolha", "dificil")[0]
        self.assertEqual(len(facil["alternativas"]), 2)
        self.assertEqual(len(dificil["alternativas"]), 4)
        for tipo in ("verdadeiro_falso", "discursiva"):
            facil = questoes_do_material(material, tipo, "facil")[0]
            dificil = questoes_do_material(material, tipo, "dificil")[0]
            self.assertNotEqual(facil["enunciado"], dificil["enunciado"])
            self.assertEqual(facil["gabarito"], dificil["gabarito"])

    def test_menu_gera_revisa_salva_e_recarrega(self):
        self.regras.return_value = {"max_questoes": 1}
        entradas = [
            "1", "10", "2", "3", "invalida", "2", "1",   # gerar, limite 1
            "2", "1", "Explique o movimento da Terra.", "", "Identificar a rotação.", "1",
            "2", "0",                                      # histórico e sair
        ]
        with patch("builtins.input", side_effect=entradas):
            provas.gerenciar_provas(self.professor)
        salva, = provas.listar_historico(2, usuario=self.professor)
        self.assertEqual(self.registros(), [salva])
        self.assertEqual(salva["questoes"][0]["enunciado"], "Explique o movimento da Terra.")
        self.assertEqual(salva["questoes"][0]["criterio_correcao"], "Identificar a rotação.")
        self.assertEqual(salva["questoes"][0]["dificuldade"], "dificil")
        self.assertEqual((salva["professor_id"], salva["id"]), (2, 1))
        self.assertIn("máximo 1", self.saida.getvalue())
        self.assertNotIn("Pendente", self.saida.getvalue())
        self.assertNotIn("Outra turma", self.saida.getvalue())
        self.uso.assert_called_once_with(10)

    def test_descarte_limite_textual_e_material_sem_conteudo(self):
        self.regras.return_value = {"max_questoes": 20}
        with patch("builtins.input", side_effect=["10", "1", "2", "3", "2", "0"]):
            self.assertIsNone(provas.gerar_prova(self.professor))
        self.assertIn("máximo 2", self.saida.getvalue())
        self.gravar(self.materiais, [dict(self.material, conteudo_texto="", conteudo="")])
        with patch("builtins.input", side_effect=["10", "3", "1"]):
            self.assertIsNone(provas.gerar_prova(self.professor))
        self.assertEqual(self.registros(), [])
        self.uso.assert_not_called()

    def test_filtro_e_validacao_da_api_de_gravacao(self):
        for referencias in ([11], [12], [999], [True], []):
            self.assertIsNone(self.salvar(materiais_referenciados=referencias))
        self.assertIsNone(self.salvar(serie="9º ano"))
        self.assertIsNone(self.salvar(questoes=[self.questao] * 3))
        self.assertIsNone(self.salvar(questoes=[dict(self.questao, criterio_correcao=" ")]))
        self.assertIsNone(self.salvar(modelo_padrao="desconhecido"))
        self.assertIsNone(provas.salvar_prova(2, self.dados, usuario=self.coord))
        self.assertIsNone(provas.salvar_prova(1, dict(self.dados, materiais_referenciados=[11]), usuario=self.coord))
        self.assertEqual(self.registros(), [])
        self.uso.assert_not_called()
        valida = self.salvar(materiais_referenciados=[13, 10, 13])
        self.assertEqual(valida["materiais_referenciados"], [13, 10])
        self.assertEqual(self.uso.call_args_list, [call(13), call(10)])

    def test_revalida_fonte_antes_de_salvar(self):
        def revogar(prova):
            self.gravar(self.materiais, [dict(self.material, status_validacao="pendente")])
            return prova
        with patch("builtins.input", side_effect=["10", "2", "1", "1"]):
            with patch.object(provas, "editar_prova_gerada", side_effect=revogar):
                self.assertIsNone(provas.gerar_prova(self.professor))
        self.assertEqual(self.registros(), [])
        self.uso.assert_not_called()

    def test_identidade_sessao_e_desativacao(self):
        prova = self.salvar()
        self.assertIsNone(provas.salvar_prova(2, self.dados))
        for sessao in (None, self.outro, dict(self.outro, perfil="coordenacao"), dict(self.coord, perfil="professor"),
                       {"id": 999, "perfil": "coordenacao", "ativo": True}):
            self.assertFalse(provas.editar_questao(2, 1, 0, self.questao, usuario=sessao))
            self.assertFalse(provas.excluir_prova(1, 2, usuario=sessao))
            self.assertEqual(provas.exportar_prova(1, sessao), [])
            self.assertEqual(provas.listar_historico(2, usuario=sessao), [])
        self.gravar(self.usuarios, [dict(self.professor, ativo=False), self.coord])
        self.assertIsNone(provas.gerar_prova(self.professor))
        self.assertFalse(provas.editar_questao(2, 1, 0, self.questao, usuario=self.professor))
        self.assertFalse(provas.excluir_prova(1, 2, usuario=self.professor))
        self.assertEqual(provas.exportar_prova(1, self.professor), [])
        self.assertEqual(provas.listar_historico(2, usuario=self.professor), [])
        self.assertIsNone(self.salvar())
        self.assertEqual(self.registros(), [prova])
        self.exportar.assert_not_called()
        self.uso.assert_called_once_with(10)

    def test_operacoes_sobre_historico_sem_material_atual(self):
        prova = self.salvar()
        self.gravar(self.materiais, [dict(self.material, status_validacao="pendente")])
        self.assertEqual(provas.listar_historico(usuario=self.coord), [prova])
        self.assertEqual(provas.exportar_prova(1, self.professor), ["aluno", "gabarito"])
        self.exportar.assert_called_once_with(prova)
        editada = dict(self.questao, enunciado="Outra pergunta revisada")
        for indice in [-1, 1, True]:
            self.assertFalse(provas.editar_questao(2, 1, indice, editada, usuario=self.professor))
        self.assertTrue(provas.editar_questao(2, 1, 0, editada, usuario=self.coord))
        with patch("builtins.input", return_value="n"):
            self.assertFalse(provas.excluir_prova(1, 2, usuario=self.professor))
        salva, = self.registros()
        self.assertEqual(salva, dict(prova, questoes=[editada]))
        self.assertEqual(provas.exportar_prova(1, self.coord), ["aluno", "gabarito"])
        self.exportar.assert_called_with(salva)
        with patch("builtins.input", return_value="s"):
            self.assertTrue(provas.excluir_prova(1, 2, usuario=self.coord))
        self.assertEqual(self.registros(), [])
        self.uso.assert_called_once_with(10)

    def test_historico_preserva_ids_datas_e_campos_antigos(self):
        antiga = dict(self.dados, id=57, professor_id=2, data_criacao="17/10/2025 14:00", campo_legado="A")
        outra = dict(antiga, id=104, professor_id=3, questoes=[dict(self.questao, gabarito=4)])
        self.gravar(self.atividades, [antiga, outra])
        nova = self.salvar()
        self.assertEqual(nova["id"], 105)
        self.assertEqual(self.registros()[:2], [antiga, outra])
        self.assertEqual(provas.listar_historico(usuario=self.professor), [nova, antiga])
        self.assertEqual(provas.listar_historico(3, usuario=self.coord), [outra])
        self.assertEqual(provas.listar_historico(usuario=self.coord), [nova, outra, antiga])

    def test_edita_alternativas_e_confere_o_gabarito(self):
        questao = questoes_do_material(self.material, "multipla_escolha", "media")[0]
        dados = dict(self.dados, questoes=[questao])
        with patch("builtins.input", side_effect=["2", "1", "", "move", "", "", "move", "", "1"]):
            revisada = provas.editar_prova_gerada(dados)
        self.assertEqual(revisada["questoes"][0]["gabarito"], "move")
        self.assertIn("move", revisada["questoes"][0]["alternativas"])
        self.assertEqual(questao["gabarito"], "gira")
        self.assertFalse(questao_valida(dict(questao, gabarito="Marte")))
        self.assertFalse(questao_valida(dict(questao, alternativas=["gira", "GIRA"])))

    def test_erro_de_gravacao_nao_conta_uso_e_libera_temporario(self):
        with patch.object(provas.os, "replace", side_effect=OSError("falha simulada")):
            self.assertIsNone(self.salvar())
        self.assertEqual(self.registros(), [])
        self.uso.assert_not_called()
        self.assertIsNotNone(self.salvar())
        self.uso.assert_called_once_with(10)

    def test_falha_na_contagem_preserva_a_prova_ja_gravada(self):
        self.uso.side_effect = OSError("biblioteca indisponível")
        salva = self.salvar()
        self.assertEqual(self.registros(), [salva])
        self.assertIn("Falha ao contar uso", self.saida.getvalue())
        self.uso.assert_called_once_with(10)

    def test_corrupcao_nao_sobrescreve_historico(self):
        for texto in ('{"arquivo":', '{}', '[{"id":1}]', '[false]'):
            self.atividades.write_text(texto, encoding="utf-8")
            self.assertIsNone(self.salvar())
            self.assertEqual(provas.listar_historico(usuario=self.coord), [])
            self.assertEqual(provas.exportar_prova(1, self.professor), [])
            self.assertEqual(self.atividades.read_text(encoding="utf-8"), texto)
        self.uso.assert_not_called()

    def test_edicao_concorrente_durante_confirmacao_nao_se_perde(self):
        atual = self.salvar()
        edicao = dict(atual, questoes=[dict(self.questao, enunciado="Editada em outra sessão")])
        def confirmar(pergunta):
            self.gravar(self.atividades, [edicao])
            return "s"
        with patch("builtins.input", side_effect=confirmar):
            self.assertFalse(provas.excluir_prova(1, 2, usuario=self.professor))
        self.assertEqual(self.registros(), [edicao])
        self.assertTrue(provas.editar_questao(2, 1, 0, self.questao, usuario=self.professor))
        self.uso.assert_called_once_with(10)


if __name__ == "__main__":
    unittest.main()
