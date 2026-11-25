"""Autenticação com arquivos temporários, sem alterar os cadastros da escola."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from usuarios import usuarios
import configurar_acesso


class TestLogin(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.arquivo = Path(pasta.name) / "usuarios.json"
        registros = [
            {"id": 1, "nome": "Coord Teste", "email": "coord@example.test", "perfil": "coordenacao",
             "ativo": True, "turmas_lecionadas": [], "atribuicoes": []},
            {"id": 2, "nome": "Prof Teste", "email": "prof@example.test", "perfil": "professor",
             "ativo": True, "turmas_lecionadas": ["6A_CIEN"]},
        ]
        self.arquivo.write_text(json.dumps(registros), encoding="utf-8")
        ajuste = patch.object(usuarios, "ARQUIVO_USUARIOS", str(self.arquivo))
        ajuste.start()
        self.addCleanup(ajuste.stop)
        self.saida = io.StringIO()
        self.redirecionamento = redirect_stdout(self.saida)
        self.redirecionamento.__enter__()
        self.addCleanup(self.redirecionamento.__exit__, None, None, None)

    def iniciar(self):
        return usuarios.configurar_primeiro_acesso("coord@example.test", "Coordenacao123!")

    def test_hash_tem_salt_e_nao_guarda_texto_puro(self):
        primeiro = usuarios.preparar_senha("SenhaTeste123!")
        segundo = usuarios.preparar_senha("SenhaTeste123!")
        self.assertNotEqual(primeiro, segundo)
        self.assertTrue(usuarios.conferir_senha(primeiro, "SenhaTeste123!"))
        self.assertFalse(usuarios.conferir_senha(primeiro, "errada"))
        self.assertNotIn("SenhaTeste123!", json.dumps(primeiro))

    def test_configuracao_preserva_dados_e_nao_pode_ser_repetida(self):
        antes = json.loads(self.arquivo.read_text(encoding="utf-8"))
        self.iniciar()
        novos = usuarios.carregar_usuarios()
        for antigo, novo in zip(antes, novos):
            for campo, valor in antigo.items():
                self.assertEqual(novo[campo], valor)
        gravado = self.arquivo.read_bytes()
        with self.assertRaisesRegex(ValueError, "já foi configurado"):
            usuarios.configurar_primeiro_acesso("coord@example.test", "OutraSenha123!")
        self.assertEqual(self.arquivo.read_bytes(), gravado)
        self.assertNotIn(b"Coordenacao123!", gravado)

    def test_primeiro_acesso_aceita_email_pessoal_e_preserva_id_e_perfil(self):
        antes = usuarios.carregar_usuarios()
        with patch("builtins.input", return_value="  pessoal@example.test  "), \
                patch.object(usuarios, "ler_senha", return_value="MinhaSenha123!"):
            configurar_acesso.configurar_acesso()
        novos = usuarios.carregar_usuarios()
        self.assertEqual(novos[0]["email"], "pessoal@example.test")
        for campo in ("id", "nome", "perfil", "ativo", "turmas_lecionadas", "atribuicoes"):
            self.assertEqual(novos[0][campo], antes[0][campo])
        self.assertEqual(novos[1], antes[1])
        with patch("builtins.input", return_value="pessoal@example.test"), \
                patch.object(usuarios, "ler_senha", return_value="MinhaSenha123!"):
            self.assertEqual(usuarios.fazer_login()["id"], 1)
        with patch("builtins.input", side_effect=AssertionError("Não deve pedir nova configuração")):
            configurar_acesso.configurar_acesso()

    def test_primeiro_acesso_rejeita_email_duplicado_ou_invalido(self):
        antes = self.arquivo.read_bytes()
        for email in ("prof@example.test", "sem-email", "nome @example.test"):
            with self.assertRaises(ValueError):
                usuarios.configurar_primeiro_acesso(email, "MinhaSenha123!", "coord@example.test")
            self.assertEqual(self.arquivo.read_bytes(), antes)

    def test_cancelar_configuracao_nao_pede_senha_nem_altera_cadastro(self):
        antes = self.arquivo.read_bytes()
        with patch("builtins.input", return_value="0"), patch.object(usuarios, "ler_senha") as senha:
            configurar_acesso.configurar_acesso()
            senha.assert_not_called()
        self.assertEqual(self.arquivo.read_bytes(), antes)

    def test_sem_senhas_login_orienta_configuracao_sem_listar_contas(self):
        with patch("builtins.input", side_effect=AssertionError("Não deve iniciar login sem configuração")):
            self.assertIsNone(usuarios.fazer_login())
        self.assertIn("configurar_acesso.py", self.saida.getvalue())
        self.assertNotIn("coord@example.test", self.saida.getvalue())
        self.assertNotIn("Coord Teste", self.saida.getvalue())
        with self.assertRaises(ValueError):
            usuarios.configurar_primeiro_acesso("prof@example.test", "SenhaTeste123!")

    def test_login_exige_email_e_senha_e_nao_exibe_outros_usuarios(self):
        self.iniciar()
        with patch("builtins.input", side_effect=["1", "coord@example.test", "  COORD@example.test  "]), \
                patch.object(usuarios, "ler_senha", side_effect=["Coordenacao123!", "errada", "Coordenacao123!"]):
            self.assertEqual(usuarios.fazer_login()["id"], 1)
        self.assertEqual(self.saida.getvalue().count("E-mail ou senha inválidos"), 2)
        self.assertNotIn("Prof Teste", self.saida.getvalue())
        self.assertNotIn("prof@example.test", self.saida.getvalue())
        with patch("builtins.input", return_value="0"), patch.object(usuarios, "ler_senha") as senha:
            self.assertIsNone(usuarios.fazer_login())
            senha.assert_not_called()

    def test_cadastro_e_redefinicao_exigem_coordenacao_e_revogam_sessao(self):
        coord = self.iniciar()
        prof = usuarios.definir_senha(2, "Professor123!", coord)
        with self.assertRaises(PermissionError):
            usuarios.definir_senha(1, "Invadindo123!", prof)
        novo = usuarios.definir_senha(2, "NovaSenha123!", coord)
        self.assertIsNone(usuarios.usuario_da_sessao(prof, usuarios.carregar_usuarios()))
        self.assertFalse(usuarios.conferir_senha(novo, "Professor123!"))
        self.assertTrue(usuarios.conferir_senha(novo, "NovaSenha123!"))
        usuarios.desativar_usuario(2, coord)
        with patch("builtins.input", side_effect=["prof@example.test", "0"]), \
                patch.object(usuarios, "ler_senha", return_value="NovaSenha123!"):
            self.assertIsNone(usuarios.fazer_login())

    def test_senha_curta_e_confirmacao_divergente_nao_alteram_json(self):
        coord = self.iniciar()
        antes = self.arquivo.read_bytes()
        with self.assertRaises(ValueError):
            usuarios.definir_senha(2, "curta", coord)
        with patch.object(usuarios, "ler_senha", side_effect=["SenhaTeste123!", "Diferente123!"]):
            with self.assertRaises(ValueError):
                usuarios.pedir_nova_senha()
        self.assertEqual(self.arquivo.read_bytes(), antes)

    def test_redefinicao_pelo_menu(self):
        coord = self.iniciar()
        with patch("builtins.input", side_effect=["6", "2", "0"]), \
                patch.object(usuarios, "ler_senha", return_value="Professor123!"):
            usuarios.gerenciar_usuarios(coord)
        prof = usuarios.buscar_usuario(usuarios.carregar_usuarios(), 2)
        self.assertTrue(usuarios.conferir_senha(prof, "Professor123!"))

    def test_hash_corrompido_e_conta_alterada_durante_login_sao_recusados(self):
        coord = self.iniciar()
        def desativar_antes_de_entrar():
            usuarios.desativar_usuario(1, coord)
            return "Coordenacao123!"
        with patch("builtins.input", return_value="coord@example.test"), \
                patch.object(usuarios, "ler_senha", side_effect=desativar_antes_de_entrar):
            self.assertIsNone(usuarios.fazer_login())
        registros = usuarios.carregar_usuarios()
        registros[0]["senha_hash"] = "x" * 64
        self.arquivo.write_text(json.dumps(registros), encoding="utf-8")
        antes = self.arquivo.read_bytes()
        with self.assertRaises(ValueError):
            usuarios.carregar_usuarios()
        self.assertEqual(self.arquivo.read_bytes(), antes)
