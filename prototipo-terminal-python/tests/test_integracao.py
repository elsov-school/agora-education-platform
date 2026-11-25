import io
import unittest
from contextlib import ExitStack, redirect_stdout
from unittest.mock import patch

import main


class TestMenus(unittest.TestCase):
    def setUp(self):
        self.coord = {"id": 1, "nome": "Coordenação", "ativo": True, "perfil": "coordenacao"}
        self.prof = {"id": 2, "nome": "Professora", "ativo": True, "perfil": "professor"}
        self.saida = io.StringIO()
        self.enterContext(redirect_stdout(self.saida))
        self.cadastro = self.enterContext(patch.object(main.usuarios, "carregar_usuarios",
                                                      return_value=[self.coord, self.prof]))
        self.carregar = self.enterContext(patch.object(main.materiais, "carregar_dados", return_value=True))

    def test_sessao_e_encaminhamento_por_perfil(self):
        rotas = [
            (main.usuarios, "gerenciar_usuarios", self.coord),
            (main.materiais, "gerenciar_materiais", self.coord),
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
                destino = pilha.enter_context(patch.object(modulo, nome, create=True))
                chamadas.append((destino, usuario))
            historico = pilha.enter_context(patch.object(main.provas, "gerenciar_provas", create=True))
            login = pilha.enter_context(patch.object(main.usuarios, "fazer_login", create=True,
                                                     side_effect=[self.coord, self.prof]))
            opcoes = ["?", "1", "2", "3", "4", "5", "6", "9", "1", "2", "3", "4", "5", "0"]
            pilha.enter_context(patch("builtins.input", side_effect=opcoes))
            main.menu_principal()

        for destino, usuario in chamadas:
            destino.assert_called_once_with(usuario)
        self.assertEqual([chamada.args for chamada in historico.call_args_list], [(self.coord,), (self.prof,)])
        self.assertEqual(login.call_count, 2)
        self.assertIn("Opção inválida", self.saida.getvalue())
        self.assertIn("Até logo!", self.saida.getvalue())

    def test_dados_invalidos_interrompem_antes_do_login(self):
        self.carregar.return_value = False
        with patch.object(main.usuarios, "fazer_login", create=True) as login:
            main.menu_principal()
        login.assert_not_called()

    def test_sair_no_login(self):
        with patch.object(main.usuarios, "fazer_login", create=True, return_value=None):
            main.menu_principal()
        self.cadastro.assert_not_called()

    def test_menus_rejeitam_perfil_incorreto_e_cadastro_desativado(self):
        self.cadastro.return_value = [dict(self.prof, ativo=False)]
        with patch("builtins.input", side_effect=AssertionError("Menu indevido")):
            main.menu_coordenacao(self.prof)
            main.menu_professor(self.prof)
        self.assertIn("Acesso restrito", self.saida.getvalue())
