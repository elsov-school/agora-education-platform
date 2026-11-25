import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import padroes
from padroes import padroes as modulo


class TestPadroes(unittest.TestCase):
    def setUp(self):
        temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(temporaria.cleanup)
        pasta = Path(temporaria.name)
        self.arquivo = pasta / "regras.json"
        self.saida = pasta / "exportacoes"
        for constante, caminho in (("ARQUIVO_REGRAS", self.arquivo),
                                   ("PASTA_EXPORTACOES", self.saida)):
            ajuste = patch.object(modulo, constante, str(caminho))
            ajuste.start()
            self.addCleanup(ajuste.stop)

        self.regras = {"nome_escola": "Escola Ipê", "max_questoes": 2,
                       "instrucoes": "Responda a lápis."}
        self.arquivo.write_text(json.dumps(self.regras, ensure_ascii=False), encoding="utf-8")
        self.coordenacao = {"id": 1, "perfil": "coordenacao", "ativo": True}
        self.cadastro = pasta / "usuarios.json"
        self.cadastro.write_text(json.dumps([self.coordenacao]), encoding="utf-8")
        usuarios = patch.object(modulo.usuarios, "ARQUIVO_USUARIOS", str(self.cadastro))
        usuarios.start()
        self.addCleanup(usuarios.stop)
        self.prova = {
            "id": 7, "serie": "6º ano", "disciplina": "Ciências", "bimestre": 1,
            "professor_id": 2, "modelo_padrao": "institucional_v1",
            "questoes": [
                {"enunciado": "Marque a opção pedida.", "tipo": "múltipla escolha",
                 "dificuldade": "fácil", "alternativas": ["Primeira opção", "B) Segunda opção"],
                 "gabarito": "Letra B", "criterio_correcao": "Validar a escolha indicada."},
                {"enunciado": "Justifique sua escolha.", "tipo": "discursiva",
                 "dificuldade": "média", "alternativas": [],
                 "gabarito": "Explicação esperada", "criterio_correcao": "Aceitar sinônimos."},
            ],
        }

    def configurar(self, usuario, entradas):
        with patch("builtins.input", side_effect=entradas), redirect_stdout(io.StringIO()):
            return padroes.configurar_padrao_escola(usuario)

    def test_configuracao_persiste_e_campos_em_branco_mantem_o_valor(self):
        novas = self.configurar(self.coordenacao, ["Colégio Ação", "3", "Leia em silêncio."])
        self.assertEqual(novas, {"nome_escola": "Colégio Ação", "max_questoes": 3,
                                 "instrucoes": "Leia em silêncio."})
        self.assertEqual(padroes.carregar_regras(), novas)
        self.assertEqual(self.configurar(self.coordenacao, ["", "", ""]), novas)

    def test_apenas_coordenacao_ativa_pode_configurar(self):
        anterior = self.arquivo.read_bytes()
        for usuario in (None, {}, {"perfil": "coordenacao"},
                        {"perfil": "coordenacao", "ativo": False},
                        {"perfil": "coordenacao", "ativo": "false"},
                        {"perfil": "professor", "ativo": True}):
            with self.subTest(usuario=usuario):
                self.assertIsNone(self.configurar(usuario, []))
                self.assertEqual(self.arquivo.read_bytes(), anterior)

    def test_sessao_antiga_perde_acesso_apos_desativacao_ou_mudanca_de_perfil(self):
        anterior = self.arquivo.read_bytes()
        for cadastro in ([], [{"id": 1, "perfil": "coordenacao", "ativo": False}],
                         [{"id": 1, "perfil": "professor", "ativo": True}]):
            with self.subTest(cadastro=cadastro):
                self.cadastro.write_text(json.dumps(cadastro), encoding="utf-8")
                self.assertIsNone(self.configurar(self.coordenacao, []))
                self.assertEqual(self.arquivo.read_bytes(), anterior)

    def test_limite_digitado_invalido_preserva_configuracao(self):
        anterior = self.arquivo.read_bytes()
        for limite in ("0", "-3", "1.5", "cinco"):
            with self.subTest(limite=limite):
                self.assertIsNone(self.configurar(self.coordenacao, ["Outra", limite]))
                self.assertEqual(self.arquivo.read_bytes(), anterior)

    def test_regras_danificadas_preservadas_e_exportacao_bloqueada(self):
        for conteudo in (b"{", b"\xff", b"[]", b"{}",
                         b'{"nome_escola":"X","instrucoes":"Y","max_questoes":true}'):
            with self.subTest(conteudo=conteudo):
                self.arquivo.write_bytes(conteudo)
                with self.assertRaises(ValueError):
                    padroes.carregar_regras()
                self.assertIsNone(self.configurar(self.coordenacao, []))
                with self.assertRaises(ValueError):
                    padroes.exportar_prova_formatada(self.prova)
                self.assertEqual(self.arquivo.read_bytes(), conteudo)
                self.assertFalse(self.saida.exists())

    def test_exportacao_separa_respostas_e_preserva_ordem_e_alternativas(self):
        caminhos = padroes.exportar_prova_formatada(self.prova)
        self.assertEqual(caminhos, [str(self.saida / "prova_aluno_7.txt"),
                                    str(self.saida / "gabarito_professor_7.txt")])
        aluno, professor = [Path(c).read_text(encoding="utf-8") for c in caminhos]
        for trecho in ("Escola Ipê", "Ciências", "6º ano", "Professor ID: 2"):
            self.assertIn(trecho, aluno)
            self.assertIn(trecho, professor)
        self.assertIn("Responda a lápis.", aluno)
        self.assertIn("A) Primeira opção", aluno)
        self.assertIn("   B) Segunda opção", aluno)
        self.assertLess(aluno.index("1. Marque"), aluno.index("2. Justifique"))
        self.assertNotIn("GABARITO", aluno)
        for numero, questao in enumerate(self.prova["questoes"], 1):
            self.assertNotIn(questao["gabarito"], aluno)
            self.assertNotIn(questao["criterio_correcao"], aluno)
            self.assertIn(f"{numero}. {questao['gabarito']}", professor)
            self.assertIn(questao["criterio_correcao"], professor)

    def test_reexportacao_reflete_revisao_e_usa_diretorio_solicitado(self):
        destino = self.saida / "turma.6A"
        caminhos = padroes.exportar_prova_formatada(self.prova, destino)
        self.prova["questoes"][1]["enunciado"] = "Escreva uma nova justificativa."
        self.prova["questoes"][1]["gabarito"] = "Resposta revisada"
        self.assertEqual(padroes.exportar_prova_formatada(self.prova, destino), caminhos)
        self.assertEqual(len(list(destino.iterdir())), 2)
        self.assertIn("nova justificativa", Path(caminhos[0]).read_text(encoding="utf-8"))
        self.assertIn("Resposta revisada", Path(caminhos[1]).read_text(encoding="utf-8"))

    def test_prova_acima_do_limite_nao_altera_arquivos_existentes(self):
        caminhos = padroes.exportar_prova_formatada(self.prova)
        anteriores = [Path(c).read_bytes() for c in caminhos]
        self.configurar(self.coordenacao, ["", "1", ""])
        with self.assertRaisesRegex(ValueError, "limite de 1"):
            padroes.exportar_prova_formatada(self.prova)
        self.assertEqual([Path(c).read_bytes() for c in caminhos], anteriores)

    def test_questoes_invalidas_nao_geram_arquivos(self):
        for campo, valor in (("enunciado", ""), ("dificuldade", None), ("tipo", ""),
                             ("alternativas", ["Uma"]), ("alternativas", ["Uma", " "]),
                             ("gabarito", []), ("criterio_correcao", " ")):
            with self.subTest(campo=campo), patch.dict(self.prova["questoes"][0], {campo: valor}):
                with self.assertRaises(ValueError):
                    padroes.exportar_prova_formatada(self.prova)
                self.assertFalse(self.saida.exists())
        del self.prova["questoes"][0]["alternativas"]
        with self.assertRaises(ValueError):
            padroes.exportar_prova_formatada(self.prova)
        self.assertFalse(self.saida.exists())

    def test_id_e_modelo_invalidos_nao_geram_arquivos(self):
        for campo, valor in (("id", None), ("id", "../7"), ("id", True),
                             ("id", 0), ("modelo_padrao", "desconhecido")):
            with self.subTest(campo=campo), patch.dict(self.prova, {campo: valor}):
                with self.assertRaises(ValueError):
                    padroes.exportar_prova_formatada(self.prova)
                self.assertFalse(self.saida.exists())

    def test_formato_e_exportacao_anteriores_aceitam_questao_sem_detalhes(self):
        self.prova["questoes"] = [{"enunciado": "Quanto é 1 - 1?", "gabarito": 0,
                                   "criterio_correcao": "Conferir o resultado."}]
        self.assertTrue(padroes.validar_prova(self.prova))
        modelo = padroes.obter_modelo()
        modelo["campos"].clear()
        self.assertTrue(padroes.obter_modelo()["campos"])
        aluno = padroes.formatar_prova(self.prova, modelo)
        self.assertNotIn("Conferir o resultado.", aluno)
        arquivo = padroes.exportar_atividade(self.prova, self.saida)
        self.assertEqual(Path(arquivo), self.saida / "atividade_7.txt")
        self.assertEqual(Path(arquivo).read_text(encoding="utf-8"), aluno)
        arquivo = padroes.exportar_atividade(self.prova, self.saida / "revisao.v1", True)
        self.assertEqual(Path(arquivo), self.saida / "revisao.v1.txt")
        self.assertIn("Conferir o resultado.", Path(arquivo).read_text(encoding="utf-8"))

    def test_falha_ao_publicar_gabarito_desfaz_a_troca_do_aluno(self):
        caminhos = padroes.exportar_prova_formatada(self.prova)
        conteudos = [Path(c).read_bytes() for c in caminhos]
        substituir = os.replace

        def falhar_no_gabarito(origem, destino):
            if destino == caminhos[1]:
                raise PermissionError("Arquivo ocupado")
            substituir(origem, destino)

        self.prova["questoes"][1]["enunciado"] = "Novo enunciado."
        with patch.object(modulo.os, "replace", side_effect=falhar_no_gabarito):
            with self.assertRaises(PermissionError):
                padroes.exportar_prova_formatada(self.prova)
        self.assertEqual([Path(c).read_bytes() for c in caminhos], conteudos)
        self.assertEqual(len(list(self.saida.iterdir())), 2)
        Path(caminhos[0]).unlink()
        with patch.object(modulo.os, "replace", side_effect=falhar_no_gabarito):
            with self.assertRaises(PermissionError):
                padroes.exportar_prova_formatada(self.prova)
        self.assertFalse(Path(caminhos[0]).exists())

    def test_exportacoes_simultaneas_do_mesmo_id_preservam_o_preparo(self):
        preparo = self.saida / ".exportando_7"
        preparo.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            padroes.exportar_prova_formatada(self.prova)
        self.assertEqual(list(self.saida.iterdir()), [preparo])


if __name__ == "__main__":
    unittest.main()
