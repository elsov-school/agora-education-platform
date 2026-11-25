import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import ExitStack, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class TestMenus(unittest.TestCase):
    def setUp(self):
        self.patches = ExitStack()
        self.addCleanup(self.patches.close)
        self.coord = {"id": 1, "nome": "Coordenação", "ativo": True, "perfil": "coordenacao"}
        self.prof = {"id": 2, "nome": "Professora", "ativo": True, "perfil": "professor"}
        self.saida = io.StringIO()
        self.patches.enter_context(redirect_stdout(self.saida))
        self.cadastro = self.patches.enter_context(patch.object(main.usuarios, "carregar_usuarios",
                                                      return_value=[self.coord, self.prof]))
        self.carregar = self.patches.enter_context(patch.object(main.materiais, "carregar_dados", return_value=True))

    def test_sessao_e_encaminhamento_por_perfil(self):
        rotas = [
            (main.usuarios, "gerenciar_usuarios", self.coord),
            (main.materiais, "aprovar_materiais_pendentes", self.coord),
            (main.padroes, "configurar_padrao_escola", self.coord),
            (main, "menu_painel", self.coord),
            (main.consultas, "pesquisar_material", self.prof),
            (main.materiais, "adicionar_material", self.prof),
            (main.consultas, "consultar_com_evidencia", self.prof),
            (main.provas, "gerar_prova", self.prof)
        ]
        with ExitStack() as pilha:
            chamadas = []
            for modulo, nome, usuario in rotas:
                destino = pilha.enter_context(patch.object(modulo, nome))
                chamadas.append((destino, usuario))
            biblioteca = pilha.enter_context(patch.object(main.materiais, "gerenciar_materiais"))
            historico = pilha.enter_context(patch.object(main.provas, "gerenciar_provas"))
            login = pilha.enter_context(patch.object(main.usuarios, "fazer_login",
                                                     side_effect=[self.coord, self.prof]))
            opcoes = ["?", "1", "2", "3", "4", "5", "6", "9", "1", "2", "3", "4", "5", "6", "0"]
            pilha.enter_context(patch("builtins.input", side_effect=opcoes))
            main.menu_principal()

        for destino, usuario in chamadas:
            destino.assert_called_once_with(usuario)
        self.assertEqual([chamada.args for chamada in historico.call_args_list], [(self.coord,), (self.prof,)])
        self.assertEqual([chamada.args for chamada in biblioteca.call_args_list], [(self.coord,), (self.prof,)])
        self.assertEqual(login.call_count, 2)
        self.assertIn("Opção inválida", self.saida.getvalue())
        self.assertIn("Até logo!", self.saida.getvalue())

    def test_dados_invalidos_interrompem_antes_do_login(self):
        self.carregar.return_value = False
        with patch.object(main.usuarios, "fazer_login") as login:
            main.menu_principal()
        login.assert_not_called()

    def test_sair_no_login(self):
        with patch.object(main.usuarios, "fazer_login", return_value=None):
            main.menu_principal()
        self.cadastro.assert_not_called()

    def test_menus_rejeitam_perfil_incorreto_e_cadastro_desativado(self):
        self.cadastro.return_value = [dict(self.prof, ativo=False)]
        with patch("builtins.input", side_effect=AssertionError("Menu indevido")):
            main.menu_coordenacao(self.prof)
            main.menu_professor(self.prof)
        self.assertIn("Acesso restrito", self.saida.getvalue())


class TestEscolaTemporaria(unittest.TestCase):
    """Cada chamada abre o main.py em outro processo, com os mesmos JSONs temporários."""

    def setUp(self):
        temporaria = tempfile.TemporaryDirectory()
        self.addCleanup(temporaria.cleanup)
        self.escola = Path(temporaria.name) / "escola"
        origem = Path(main.__file__).parent
        shutil.copytree(origem, self.escola, ignore=shutil.ignore_patterns("__pycache__", "tests", "*.txt"))
        self.gravar("usuarios/usuarios.json", [
            {"id": 1, "nome": "Coordenação", "perfil": "coordenacao", "email": "coord@example.org",
             "ativo": True, "turmas_lecionadas": [], "atribuicoes": []}
        ])
        self.gravar("materiais/materiais.json", [])
        self.gravar("provas/atividades.json", [])

    def gravar(self, caminho, dados):
        (self.escola / caminho).write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    def ler(self, caminho):
        return json.loads((self.escola / caminho).read_text(encoding="utf-8"))

    def terminal(self, *entradas):
        ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
        processo = subprocess.run(
            [sys.executable, "-B", "main.py"], cwd=self.escola, env=ambiente,
            input="\n".join(entradas) + "\n", capture_output=True,
            encoding="utf-8", timeout=15
        )
        self.assertEqual(processo.returncode, 0, processo.stdout + processo.stderr)
        self.assertIn("Até logo!", processo.stdout, processo.stdout)
        return processo.stdout

    def test_roteiro_da_escola_apos_reiniciar(self):
        # Fontes de outra turma, outra disciplina e outra série, todas já aprovadas.
        base = {"disciplina": "Ciências", "serie": "6º ano", "turma": "6A",
                "bimestre": "1º Bimestre", "tipo": "capitulo", "autor_upload": 1, "usos": 0,
                "bncc": "EF06CI01", "habilidade_bncc": "EF06CI01",
                "conteudo": "Amostra de controle.", "conteudo_texto": "Amostra de controle.",
                "status_validacao": "aprovado_coordenacao"}
        self.gravar("materiais/materiais.json", [
            dict(base, id=11, titulo="Amostra de outra turma", turma="6B"),
            dict(base, id=12, titulo="Amostra de outra disciplina", disciplina="Matemática"),
            dict(base, id=13, titulo="Amostra de outra série", serie="7º ano")
        ])
        self.terminal("1", "1",
                      "1", "Docente", "docente@example.org", "6A | 6º ano | Ciências",
                      "1", "Colega", "colega@example.org", "6A | 6º ano | Ciências", "0",
                      "4", "Escola de teste", "2", "Leia e responda.", "0")
        professor = self.ler("usuarios/usuarios.json")[1]
        self.assertEqual(professor["atribuicoes"], [{"turma": "6A", "serie": "6º ano", "disciplina": "Ciências"}])
        self.assertEqual(self.ler("padroes/regras.json")["max_questoes"], 2)

        texto = "Amostra de solo contém grãos minerais. A água atravessa os espaços entre os grãos."
        self.terminal("2", "2", "Amostra de solo", "3", "6º ano", "1", "EF06CI01",
                      texto, "2", "6A", "0")
        material = self.ler("materiais/materiais.json")[-1]
        mid = str(material["id"])
        self.assertEqual((material["autor_upload"], material["status_validacao"], material["usos"]),
                         (2, "pendente", 0))
        saida = self.terminal("2", "1", "Amostra", "3", "Amostra", "0")
        self.assertIn("Nenhum material encontrado", saida)
        self.assertIn("Nenhum trecho encontrado", saida)
        self.assertNotIn("Amostra de outra", saida)
        fila = self.terminal("1", "5", "4", "0", "3", mid, "s", "0")
        self.assertIn("Amostra de solo", fila)
        pesquisa = self.terminal("2", "1", "Amostra", "0")
        self.assertIn("Amostra de solo", pesquisa)
        self.assertNotIn("Amostra de outra", pesquisa)
        self.assertEqual(self.ler("materiais/materiais.json")[-1]["usos"], 0)
        consulta = self.terminal("2", "3", "Amostra", "0")
        self.assertIn(texto, consulta)
        self.assertIn("EF06CI01", consulta)
        self.assertNotIn("Amostra de outra", consulta)
        self.assertEqual(self.ler("materiais/materiais.json")[-1]["usos"], 1)

        geracao = self.terminal("2", "4", mid, "2", "2", "3", "1",    # tipo, dificuldade e quantidade
                                "2", "1", "Como o texto descreve o solo?", "", "",
                                "1", "0")  # aprovar o rascunho e sair
        self.assertIn("Revisão da prova", geracao)
        self.assertIn("no máximo 2", geracao)
        provas = self.ler("provas/atividades.json")
        self.assertEqual(len(provas), 1)
        prova = provas[0]
        pid = str(prova["id"])
        self.assertEqual(prova["professor_id"], 2)
        self.assertEqual(prova["materiais_referenciados"], [material["id"]])
        self.assertEqual(prova["questoes"][0]["enunciado"], "Como o texto descreve o solo?")
        self.assertEqual(self.ler("materiais/materiais.json")[-1]["usos"], 2)

        # Colega com a mesma atribuição tenta abrir o histórico, editar, excluir e exportar.
        historico = self.terminal("3", "5", "2", "3", pid, "4", pid, "5", pid, "0", "0")
        self.assertIn("Nenhuma prova encontrada", historico)
        self.assertEqual(self.ler("provas/atividades.json"), provas)
        self.assertEqual(list((self.escola / "exportacoes").glob("*.txt")), [])

        autor = self.terminal("docente@example.org", "5", "2", "3", pid, "1",
                              "", "Grãos minerais.", "Reconhecer a composição indicada.",
                              "5", pid, "0", "0")
        self.assertIn("Autor 2", autor)
        questao = self.ler("provas/atividades.json")[0]["questoes"][0]
        self.assertEqual(questao["gabarito"], "Grãos minerais.")
        aluno = (self.escola / "exportacoes" / f"prova_aluno_{pid}.txt").read_text(encoding="utf-8")
        gabarito = (self.escola / "exportacoes" / f"gabarito_professor_{pid}.txt").read_text(encoding="utf-8")
        self.assertIn("ESCOLA DE TESTE", aluno)
        self.assertIn("Leia e responda.", aluno)
        self.assertIn(questao["enunciado"], aluno)
        for campo in ("gabarito", "criterio_correcao"):
            self.assertIn(questao[campo], gabarito)
            self.assertNotIn(questao[campo], aluno)

        bancos = sorted(self.escola.glob("*/*.json"))
        antes = [banco.read_bytes() for banco in bancos]
        painel = self.terminal("1", "5", "5", "0", "0")
        self.assertIn(f"[{mid}] Amostra de solo - usos: 2", painel)
        self.assertIn("Aprovados: 4", painel)
        self.assertIn("Pendentes: 0", painel)
        self.assertIn("Atividades geradas: 1", painel)
        for grupo in ("Docente", "6º ano", "Ciências"):
            self.assertRegex(painel, grupo + r"\s+1\s+\(100%\)")
        self.assertEqual(antes, [banco.read_bytes() for banco in bancos])

        self.terminal("2", "5", "4", pid, "s", "0", "0")
        self.assertEqual(self.ler("provas/atividades.json"), [])
        saida = self.terminal("1", "1", "5", "2", "0", "9", "2", "0")
        self.assertIn("Usuário não encontrado ou inativo", saida)
        self.assertFalse(self.ler("usuarios/usuarios.json")[1]["ativo"])
