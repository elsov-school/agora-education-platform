import tempfile
import unittest
from pathlib import Path

from app import create_app
from config import TIPOS_QUESTAO
from database import connect
from services import assistant as assistant_service
from services import library as library_service


class AgoraFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "test.db"
        self.app = create_app({"TESTING": True, "DATABASE": self.database, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def login(self, user_id):
        return self.client.post("/login", data={"user_id": user_id}, follow_redirects=True)

    def test_required_python_data_structures_have_real_purpose(self):
        self.assertIsInstance(TIPOS_QUESTAO, tuple)
        materials = library_service.list_materials(database_path=self.database)
        self.assertIsInstance(materials, list)
        self.assertIsInstance(materials[0], dict)
        professor = {"role": "Professor", "subjects": ["Biologia"], "classes": ["1o ano EM"]}
        result = assistant_service.answer_question(
            "Qual e a funcao da mitocondria?", "1o ano EM", "Biologia", professor, self.database
        )
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result["evidence"], list)

    def test_external_content_verification_flow(self):
        self.login(1)
        response = self.client.post("/verificar", data={
            "title": "Verificacao demonstrativa",
            "class_name": "1o ano EM",
            "subject": "Biologia",
            "material_ids": "1",
            "content": (
                "A mitocondria participa da producao de energia celular. "
                "O planeta Netuno foi descoberto por cientistas."
            ),
        }, follow_redirects=True)
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Verificacao demonstrativa", page)
        self.assertIn("Conteúdo encontrado nas fontes", page)
        self.assertIn("Não localizado", page)
        self.assertIn("Citologia: organelas celulares", page)
        verified_library = self.client.get("/biblioteca?view=verifications")
        self.assertIn(b"Verificacao demonstrativa", verified_library.data)

        activity_library = self.client.get("/biblioteca?view=activities")
        self.assertEqual(activity_library.status_code, 200)
        self.assertIn(b"Atividade de Citologia", activity_library.data)

    def test_professor_sees_only_profile_materials_and_assistant_evidence(self):
        self.login(1)
        page = self.client.get("/biblioteca")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Citologia", page.data)
        self.assertNotIn(b"Porcentagem", page.data)

        answer = self.client.post("/assistente", data={
            "class_name": "1o ano EM", "subject": "Biologia",
            "question": "Qual e a funcao da mitocondria?",
        })
        self.assertIn(b"producao de energia", answer.data)
        self.assertIn(b"Citologia: organelas celulares", answer.data)

        refusal = self.client.post("/assistente", data={
            "class_name": "1o ano EM", "subject": "Biologia",
            "question": "Quem descobriu o planeta Netuno?",
        })
        self.assertIn("evidências suficientes", refusal.get_data(as_text=True))

    def test_material_crud_as_coordinator(self):
        self.login(4)
        response = self.client.post("/biblioteca/novo", data={
            "title": "Novo material", "material_type": "Texto", "school_year": "2026",
            "class_name": "8o ano A", "subject": "Ciencias", "bimester": "3",
            "bncc": "EF08CI01", "author_source": "Coordenacao", "content": "Este conteudo apresenta uma evidencia institucional suficientemente detalhada.",
            "approval_status": "Aprovado",
        }, follow_redirects=True)
        self.assertIn(b"Novo material", response.data)
        connection = connect(self.database)
        material_id = connection.execute("SELECT id FROM materials WHERE title='Novo material'").fetchone()[0]
        connection.close()
        response = self.client.post(f"/biblioteca/{material_id}/excluir", follow_redirects=True)
        self.assertIn(b"Material excluido", response.data)

    def test_generate_edit_regenerate_and_submit_activity(self):
        self.login(1)
        response = self.client.post("/gerador", data={
            "title": "Teste integrado", "class_name": "1o ano EM", "subject": "Biologia",
            "material_ids": "1", "quantity": "2", "question_type": "Discursiva", "difficulty": "Media",
        }, follow_redirects=True)
        self.assertIn(b"Teste integrado", response.data)
        self.assertIn(b"Citologia: organelas celulares", response.data)

        connection = connect(self.database)
        activity_id = connection.execute("SELECT id FROM activities WHERE title='Teste integrado'").fetchone()[0]
        question_id = connection.execute("SELECT id FROM questions WHERE activity_id=? ORDER BY id", (activity_id,)).fetchone()[0]
        connection.close()
        edited = self.client.post(f"/questoes/{question_id}/editar", data={
            "activity_id": activity_id, "prompt": "Questao revisada", "answer": "Resposta revisada",
        }, follow_redirects=True)
        self.assertIn(b"Questao revisada", edited.data)
        swapped = self.client.post(f"/questoes/{question_id}/trocar", data={"activity_id": activity_id}, follow_redirects=True)
        self.assertIn("Questão trocada", swapped.get_data(as_text=True))
        sent = self.client.post(f"/atividades/{activity_id}/enviar", follow_redirects=True)
        self.assertIn("Pendente de validação", sent.get_data(as_text=True))

    def test_standards_limit_and_validation_dashboard_flow(self):
        self.login(4)
        saved = self.client.post("/padroes", data={
            "max_questions": "2", "allowed_types": ["Discursiva"], "default_difficulty": "Facil",
            "require_source": "on", "header_template": "Cabecalho teste", "quality_criteria": "Clareza",
            "approval_rules": "Fonte obrigatoria", "instructions": "Use as fontes.",
        }, follow_redirects=True)
        self.assertIn(b"atualizados e aplicados", saved.data)

        self.login(1)
        blocked = self.client.post("/gerador", data={
            "class_name": "1o ano EM", "subject": "Biologia", "material_ids": "1",
            "quantity": "3", "question_type": "Discursiva", "difficulty": "Facil",
        }, follow_redirects=True)
        self.assertIn(b"entre 1 e 2", blocked.data)
        blocked_type = self.client.post("/gerador", data={
            "class_name": "1o ano EM", "subject": "Biologia", "material_ids": "1",
            "quantity": "1", "question_type": "Verdadeiro ou falso", "difficulty": "Facil",
        }, follow_redirects=True)
        self.assertIn(b"nao e permitido", blocked_type.data)

        generated = self.client.post("/gerador", data={
            "title": "Para aprovacao", "class_name": "1o ano EM", "subject": "Biologia", "material_ids": "1",
            "quantity": "1", "question_type": "Discursiva", "difficulty": "Facil",
        }, follow_redirects=True)
        self.assertIn(b"Cabecalho teste", generated.data)
        connection = connect(self.database)
        activity_id = connection.execute("SELECT id FROM activities WHERE title='Para aprovacao'").fetchone()[0]
        connection.close()
        self.client.post(f"/atividades/{activity_id}/enviar")

        self.login(4)
        queue = self.client.get("/validacao")
        self.assertIn(b"Para aprovacao", queue.data)
        reviewed = self.client.post(f"/validacao/{activity_id}", data={
            "decision": "Aprovado", "note": "Alinhado ao curriculo.",
        }, follow_redirects=True)
        self.assertIn(b"Analise registrada", reviewed.data)
        dashboard = self.client.get("/coordenacao")
        self.assertIn(b"Materiais por disciplina", dashboard.data)
        self.assertIn(b"Para aprovacao", dashboard.data)


if __name__ == "__main__":
    unittest.main()
