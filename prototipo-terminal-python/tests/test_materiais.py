import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from materiais import materiais as biblioteca


COORDENACAO = {"id": 5, "perfil": "coordenacao", "ativo": True}
PROFESSOR = {"id": 9, "perfil": "professor", "ativo": True,
             "atribuicoes": [{"turma": "6A", "serie": "6º ano", "disciplina": "Ciências"}]}
CADASTRO = ["A Terra", "3", "6º ano", "1", "EF06CI01", "Texto literal.", "2", "6A"]


class TestMateriais(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.banco = Path(pasta.name) / "materiais.json"
        self.historico = Path(pasta.name) / "atividades.json"
        self.cadastro = Path(pasta.name) / "usuarios.json"
        self.registros = [
            dict(COORDENACAO, nome="Coordenação", email="coord@example.test", turmas_lecionadas=[]),
            dict(PROFESSOR, nome="Docente", email="docente@example.test", turmas_lecionadas=["6A_CIEN"]),
            dict(PROFESSOR, id=10, nome="Docente 2", email="outro@example.test", turmas_lecionadas=["6A_CIEN"]),
        ]
        self.escrever(self.cadastro, self.registros)
        self.enterContext(patch.object(biblioteca.cadastro, "ARQUIVO_USUARIOS", str(self.cadastro)))
        self.escrever(self.banco, [])
        self.escrever(self.historico, [])
        self.enterContext(patch.object(biblioteca, "ARQUIVO_DADOS", str(self.banco)))
        self.enterContext(patch.object(biblioteca, "ARQUIVO_ATIVIDADES", str(self.historico)))
        self.enterContext(patch.object(biblioteca, "_texto_lido", None))
        anteriores = biblioteca.materiais.copy()
        self.addCleanup(biblioteca.materiais.__setitem__, slice(None), anteriores)
        self.saida = self.enterContext(patch("sys.stdout", new_callable=io.StringIO))
        self.assertTrue(biblioteca.carregar_dados())

    def escrever(self, caminho, dados):
        caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    def ler(self):
        return json.loads(self.banco.read_text(encoding="utf-8"))

    def executar_acao(self, funcao, usuario, respostas):
        with patch("builtins.input", side_effect=respostas):
            return funcao(usuario)

    def test_migracao_nos_dois_sentidos_preserva_registros(self):
        original, recente = biblioteca.materiais_exemplo()[:2]
        original.update({"id": 12, "origem": "acervo"})
        recente["habilidade_bncc"] = recente.pop("bncc")
        recente["conteudo_texto"] = recente.pop("conteudo")
        recente.update({"usos": 4, "autor_upload": 23, "status_validacao": "aprovado_coordenacao",
                        "tipo": "apostila", "turma": "6B"})
        self.escrever(self.banco, [original, recente])
        lista_importada = biblioteca.materiais
        self.assertTrue(biblioteca.carregar_dados())
        primeiro, segundo = self.ler()
        for campo, valor in original.items():
            self.assertEqual(primeiro[campo], valor)
        self.assertEqual(primeiro["status_validacao"], "pendente")
        self.assertEqual(primeiro["usos"], 0)
        self.assertIsNone(primeiro["autor_upload"])
        self.assertEqual(primeiro["tipo"], "capitulo")
        for campo, valor in recente.items():
            self.assertEqual(segundo[campo], valor)
        for item in (primeiro, segundo):
            self.assertEqual(item["conteudo_texto"], item["conteudo"])
            self.assertEqual(item["habilidade_bncc"], item["bncc"])
        salvo = self.banco.read_bytes()
        self.assertTrue(biblioteca.carregar_dados())
        self.assertIs(lista_importada, biblioteca.materiais)
        self.assertEqual(lista_importada, [primeiro, segundo])
        self.assertEqual(self.banco.read_bytes(), salvo)

    def test_arquivo_ausente_inicia_exemplos_e_lista_vazia_permanece_vazia(self):
        self.banco.unlink()
        self.assertTrue(biblioteca.carregar_dados())
        self.assertEqual([item["id"] for item in self.ler()], [1, 2, 3, 4])
        self.assertTrue(all(item["status_validacao"] == "pendente" for item in self.ler()))
        self.escrever(self.banco, [])
        self.assertTrue(biblioteca.carregar_dados())
        self.assertEqual(self.ler(), [])

    def test_corrupcao_recusa_gravacoes_sem_apagar_original(self):
        exemplo = biblioteca.materiais_exemplo()[0]
        casos = ["", "{", "null", "{}", "[{}]", json.dumps([exemplo, exemplo])]
        for alteracao in ({"usos": -1}, {"usos": True}, {"tipo": "sem tipo"},
                          {"status_validacao": "talvez"}, {"habilidade_bncc": "outro"}):
            casos.append(json.dumps([dict(exemplo, **alteracao)]))
        for caso in casos:
            with self.subTest(caso=caso):
                self.banco.write_text(caso, encoding="utf-8")
                with patch("builtins.input", side_effect=AssertionError("Pergunta inesperada")):
                    self.assertFalse(biblioteca.adicionar_material(COORDENACAO))
                self.assertFalse(biblioteca.salvar_dados())
                self.assertFalse(biblioteca.registrar_uso(1))
                self.assertEqual(self.banco.read_text(encoding="utf-8"), caso)

    def test_cadastro_pela_coordenacao_valida_entrada_e_aprova(self):
        respostas = ["", CADASTRO[0], "letras", "0"] + CADASTRO[1:]
        self.assertTrue(self.executar_acao(biblioteca.adicionar_material, COORDENACAO, respostas))
        item = self.ler()[0]
        self.assertEqual(item["id"], 1)
        self.assertEqual(item["tipo"], "capitulo")
        self.assertEqual(item["turma"], "6A")
        self.assertEqual(item["status_validacao"], "aprovado_coordenacao")
        self.assertEqual(item["autor_upload"], COORDENACAO["id"])
        self.assertEqual(item["conteudo"], item["conteudo_texto"])
        self.assertEqual(item["bncc"], item["habilidade_bncc"])

    def test_sugestao_revisao_edicao_e_nova_aprovacao(self):
        self.assertTrue(self.executar_acao(biblioteca.adicionar_material, PROFESSOR, CADASTRO))
        item = self.ler()[0]
        self.assertEqual(item["status_validacao"], "pendente")
        self.assertEqual(item["autor_upload"], PROFESSOR["id"])
        for respostas in (["abc"], ["9999"], ["1", "n"]):
            self.assertFalse(self.executar_acao(biblioteca.aprovar_materiais_pendentes, COORDENACAO, respostas))
            self.assertEqual(self.ler()[0], item)
        self.assertTrue(self.executar_acao(biblioteca.aprovar_materiais_pendentes, COORDENACAO, ["1", "s"]))
        self.assertTrue(biblioteca.registrar_uso(1))
        # Neste teste do módulo, o filtro de usuários já devolveu o material aprovado.
        with patch.object(biblioteca.cadastro, "filtrar_materiais_do_professor",
                          create=True, return_value=biblioteca.materiais) as filtro:
            outro = dict(PROFESSOR, id=10)
            self.assertFalse(self.executar_acao(biblioteca.editar_material, outro, ["1"]))
            respostas = ["1", "", "", "", "", "BNCC revisada", "Conteúdo revisto", "", "-"]
            self.assertTrue(self.executar_acao(biblioteca.editar_material, PROFESSOR, respostas))
            filtro.assert_called_with(PROFESSOR, biblioteca.materiais)
        item = self.ler()[0]
        self.assertEqual(item["bncc"], item["habilidade_bncc"])
        self.assertEqual(item["conteudo_texto"], "Conteúdo revisto")
        self.assertEqual(item["conteudo"], item["conteudo_texto"])
        self.assertEqual(item["status_validacao"], "pendente")
        self.assertEqual(item["usos"], 1)
        self.assertEqual(item["autor_upload"], PROFESSOR["id"])
        self.assertFalse(item["turma"])
        self.assertTrue(self.executar_acao(biblioteca.aprovar_materiais_pendentes, COORDENACAO, ["1", "s"]))
        self.assertEqual(self.ler()[0]["status_validacao"], "aprovado_coordenacao")

    def test_menu_e_busca_do_professor_usam_somente_a_lista_filtrada(self):
        self.escrever(self.banco, biblioteca.materiais_exemplo())
        with patch.object(biblioteca.cadastro, "filtrar_materiais_do_professor",
                          create=True, return_value=[]) as filtro:
            self.executar_acao(biblioteca.gerenciar_materiais, PROFESSOR, ["1", "1", "0"])
            self.assertTrue(filtro.called)
        self.assertNotIn("Sistema Solar", self.saida.getvalue())
        self.assertIn("Material não encontrado", self.saida.getvalue())
        self.assertNotIn("Aprovar material pendente", self.saida.getvalue())

    def test_operacoes_protegidas_verificam_perfil_e_sessao(self):
        usuarios = [None, {}, dict(PROFESSOR, ativo=False), dict(COORDENACAO, ativo=False),
                    dict(PROFESSOR, perfil="aluno")]
        with patch("builtins.input", side_effect=AssertionError("Acesso indevido")):
            for usuario in usuarios:
                for operacao in (biblioteca.adicionar_material, biblioteca.editar_material,
                                 biblioteca.excluir_material, biblioteca.aprovar_materiais_pendentes,
                                 biblioteca.gerenciar_materiais, biblioteca.visualizar_material):
                    self.assertFalse(operacao(usuario))
            self.assertFalse(biblioteca.excluir_material(PROFESSOR))
            self.assertFalse(biblioteca.aprovar_materiais_pendentes(PROFESSOR))
        self.assertEqual(self.ler(), [])

    def test_revalida_perfil_e_atividade_antes_de_operar_e_de_gravar(self):
        self.registros[0]["ativo"] = False
        self.escrever(self.cadastro, self.registros)
        with patch("builtins.input", side_effect=AssertionError("Sessão sem permissão")):
            self.assertFalse(biblioteca.aprovar_materiais_pendentes(COORDENACAO))
            self.assertFalse(biblioteca.adicionar_material(dict(PROFESSOR, perfil="coordenacao")))

        respostas = iter(CADASTRO)
        def responder(pergunta):
            if pergunta.startswith("Turma"):
                self.registros[1]["ativo"] = False
                self.escrever(self.cadastro, self.registros)
            return next(respostas)

        with patch("builtins.input", side_effect=responder):
            self.assertFalse(biblioteca.adicionar_material(PROFESSOR))
        self.assertEqual(self.ler(), [])

    def test_exclusao_exige_confirmacao_e_preserva_historico(self):
        self.assertTrue(self.executar_acao(biblioteca.adicionar_material, COORDENACAO, CADASTRO))
        original = self.banco.read_bytes()
        self.historico.unlink()
        for historico in (None, "{", "{}", "[{}]", '[{"materiais_referenciados":["1"]}]',
                          '[{"materiais_referenciados":[1]}]'):
            if historico is not None:
                self.historico.write_text(historico, encoding="utf-8")
            self.assertFalse(self.executar_acao(biblioteca.excluir_material, COORDENACAO, ["1", "s"]))
            self.assertEqual(self.banco.read_bytes(), original)
        self.escrever(self.historico, [{"materiais_referenciados": [9]}])
        self.assertFalse(self.executar_acao(biblioteca.excluir_material, COORDENACAO, ["1", "n"]))
        self.assertEqual(self.banco.read_bytes(), original)
        self.assertTrue(self.executar_acao(biblioteca.excluir_material, COORDENACAO, ["1", "s"]))
        self.assertTrue(biblioteca.carregar_dados())
        self.assertEqual(self.ler(), [])

    def test_contador_rele_arquivo_e_preserva_outras_mudancas(self):
        self.escrever(self.banco, biblioteca.materiais_exemplo()[:2])
        self.assertTrue(biblioteca.carregar_dados())
        atual = self.ler()
        atual[0].update({"usos": 7, "titulo": "Revisado em outro terminal"})
        atual[1]["usos"] = 5
        self.escrever(self.banco, atual)
        self.assertTrue(biblioteca.registrar_uso(atual[0]["id"]))
        atual[0]["usos"] += 1
        self.assertEqual(self.ler(), atual)
        self.assertEqual(biblioteca.materiais, atual)
        for identificador in (None, True, "1", -1, 999):
            self.assertFalse(biblioteca.registrar_uso(identificador))
        self.assertEqual(self.ler(), atual)

    def test_contador_soma_ao_incremento_concorrente(self):
        self.assertTrue(self.executar_acao(biblioteca.adicionar_material, COORDENACAO, CADASTRO))
        gravar = biblioteca._gravar
        chamadas = []

        def outro_uso_antes_da_primeira_gravacao(novos, versao):
            if not chamadas:
                atual = self.ler()
                atual[0]["usos"] += 1
                self.escrever(self.banco, atual)
            chamadas.append(1)
            gravar(novos, versao)

        with patch.object(biblioteca, "_gravar", side_effect=outro_uso_antes_da_primeira_gravacao):
            self.assertTrue(biblioteca.registrar_uso(1))
        self.assertEqual(self.ler()[0]["usos"], 2)
        self.assertEqual(biblioteca.materiais, self.ler())

    def test_falha_de_escrita_e_edicao_desatualizada_preservam_o_disco(self):
        original = self.banco.read_bytes()
        with patch.object(os, "replace", side_effect=OSError("falha de gravação")):
            self.assertFalse(self.executar_acao(biblioteca.adicionar_material, COORDENACAO, CADASTRO))
        self.assertEqual(self.banco.read_bytes(), original)
        self.assertEqual(biblioteca.materiais, [])
        self.assertFalse(Path(str(self.banco) + ".tmp").exists())
        self.assertTrue(self.executar_acao(biblioteca.adicionar_material, COORDENACAO, CADASTRO))
        atual = self.ler()
        atual[0]["usos"] += 1
        self.escrever(self.banco, atual)
        self.assertFalse(biblioteca.salvar_dados())
        self.assertEqual(self.ler(), atual)
