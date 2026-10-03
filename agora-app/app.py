import json
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from config import DATABASE_PATH, DIFICULDADES, SECRET_KEY, TIPOS_QUESTAO
from database import connect, init_database
from services import assistant as assistant_service
from services import dashboard as dashboard_service
from services import generator as generator_service
from services import library as library_service
from services import standards as standards_service
from services import validation as validation_service
from services import verifier as verifier_service


DISPLAY_LABELS = {
    "Coordenacao": "Coordenação",
    "Pendente de validacao": "Pendente de validação",
    "Multipla escolha": "Múltipla escolha",
    "Facil": "Fácil",
    "Media": "Média",
    "Dificil": "Difícil",
    "Matematica": "Matemática",
    "Portugues": "Português",
    "Ciencias": "Ciências",
}


def display_label(value):
    label = DISPLAY_LABELS.get(value, value)
    if not isinstance(label, str):
        return label
    return label.replace("1o ano", "1º ano").replace("8o ano", "8º ano").replace("9o ano", "9º ano")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=SECRET_KEY, DATABASE=DATABASE_PATH)
    if test_config:
        app.config.update(test_config)
    app.jinja_env.filters["label"] = display_label
    init_database(app.config["DATABASE"])

    def database_path():
        return app.config["DATABASE"]

    def current_user():
        user_id = session.get("user_id")
        if not user_id:
            return None
        connection = connect(database_path())
        row = connection.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        connection.close()
        if not row:
            return None
        user = dict(row)
        user["subjects"] = json.loads(user["subjects"])
        user["classes"] = json.loads(user["classes"])
        return user

    def login_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user():
                flash("Escolha um perfil para continuar.", "info")
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    def role_required(role):
        def decorator(view):
            @wraps(view)
            def wrapped(*args, **kwargs):
                user = current_user()
                if not user:
                    return redirect(url_for("login"))
                if user["role"] != role:
                    flash("Seu perfil não possui acesso a esta área.", "error")
                    return redirect(url_for("home"))
                return view(*args, **kwargs)
            return wrapped
        return decorator

    @app.context_processor
    def inject_globals():
        return {"current_user": current_user(), "TIPOS_QUESTAO": TIPOS_QUESTAO, "DIFICULDADES": DIFICULDADES}

    @app.route("/")
    def index():
        return redirect(url_for("home" if current_user() else "login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        connection = connect(database_path())
        users = [dict(row) for row in connection.execute("SELECT * FROM users ORDER BY role, name").fetchall()]
        connection.close()
        for user in users:
            user["subjects"] = json.loads(user["subjects"])
            user["classes"] = json.loads(user["classes"])
        if request.method == "POST":
            try:
                user_id = int(request.form["user_id"])
            except (KeyError, ValueError):
                flash("Selecione um perfil valido.", "error")
                return render_template("login.html", users=users)
            if not any(user["id"] == user_id for user in users):
                abort(400)
            session.clear()
            session["user_id"] = user_id
            flash("Perfil de demonstração ativado.", "success")
            return redirect(url_for("home"))
        return render_template("login.html", users=users)

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/inicio")
    @login_required
    def home():
        user = current_user()
        if user["role"] == "Coordenacao":
            return redirect(url_for("dashboard"))
        activities = generator_service.list_teacher_activities(user["id"], database_path())
        approved_materials = library_service.list_materials(user=user, approved_only=True, database_path=database_path())
        verifications = verifier_service.list_verifications(user["id"], database_path())
        return render_template(
            "teacher_home.html", activities=activities, verifications=verifications,
            material_count=len(approved_materials), materials=approved_materials,
        )

    @app.post("/criar")
    @role_required("Professor")
    def create_from_prompt():
        prompt = request.form.get("prompt", "").strip()
        intent = request.form.get("intent", "activity")
        if prompt:
            session["creation_prompt"] = prompt
        if intent == "verify":
            return redirect(url_for("verify_content"))
        if intent == "consult":
            return redirect(url_for("assistant"))
        return redirect(url_for("generator"))

    @app.route("/biblioteca")
    @login_required
    def library():
        user = current_user()
        filters = {key: request.args.get(key, "").strip() for key in ("search", "subject", "class_name", "bimester", "bncc")}
        materials = library_service.list_materials(filters, user=user, database_path=database_path())
        visible_all = library_service.list_materials(user=user, database_path=database_path())
        options = {
            "subjects": sorted({item["subject"] for item in visible_all}),
            "classes": sorted({item["class_name"] for item in visible_all}),
            "bimesters": sorted({item["bimester"] for item in visible_all}),
        }
        activities = generator_service.list_teacher_activities(user["id"], database_path()) if user["role"] == "Professor" else []
        verifications = verifier_service.list_verifications(user["id"], database_path()) if user["role"] == "Professor" else []
        return render_template(
            "library.html", materials=materials, filters=filters, options=options,
            activities=activities, verifications=verifications, view=request.args.get("view", "materials"),
        )

    @app.route("/biblioteca/novo", methods=["GET", "POST"])
    @role_required("Coordenacao")
    def material_new():
        if request.method == "POST":
            try:
                material_id = library_service.save_material(_material_form_data(), database_path=database_path())
                flash("Material cadastrado com sucesso.", "success")
                return redirect(url_for("material_detail", material_id=material_id))
            except (KeyError, ValueError) as error:
                flash(str(error) or "Preencha todos os campos.", "error")
        return render_template("material_form.html", material=None)

    def _material_form_data():
        required = ("title", "material_type", "school_year", "class_name", "subject", "bimester", "bncc", "author_source", "content", "approval_status")
        result = {key: request.form.get(key, "").strip() for key in required}
        if not all(result.values()):
            raise ValueError("Preencha todos os campos obrigatórios.")
        result["school_year"] = int(result["school_year"])
        result["bimester"] = int(result["bimester"])
        if result["bimester"] not in range(1, 5):
            raise ValueError("O bimestre deve estar entre 1 e 4.")
        if result["approval_status"] not in ("Aprovado", "Pendente", "Reprovado"):
            raise ValueError("Status de aprovação inválido.")
        return result

    @app.route("/biblioteca/<int:material_id>")
    @login_required
    def material_detail(material_id):
        material = library_service.get_material(material_id, database_path())
        if not material:
            abort(404)
        user = current_user()
        if user["role"] == "Professor" and (material["subject"] not in user["subjects"] or material["class_name"] not in user["classes"]):
            abort(403)
        return render_template("material_detail.html", material=material)

    @app.route("/biblioteca/<int:material_id>/editar", methods=["GET", "POST"])
    @role_required("Coordenacao")
    def material_edit(material_id):
        material = library_service.get_material(material_id, database_path())
        if not material:
            abort(404)
        if request.method == "POST":
            try:
                library_service.save_material(_material_form_data(), material_id, database_path())
                flash("Material atualizado.", "success")
                return redirect(url_for("material_detail", material_id=material_id))
            except (ValueError, KeyError) as error:
                flash(str(error), "error")
        return render_template("material_form.html", material=material)

    @app.post("/biblioteca/<int:material_id>/excluir")
    @role_required("Coordenacao")
    def material_delete(material_id):
        try:
            library_service.delete_material(material_id, database_path())
            flash("Material excluido.", "success")
        except Exception:
            flash("O material possui vinculos e nao pode ser excluido.", "error")
        return redirect(url_for("library"))

    @app.route("/gerador", methods=["GET", "POST"])
    @role_required("Professor")
    def generator():
        user = current_user()
        settings = standards_service.get_settings(database_path())
        materials = library_service.list_materials(user=user, approved_only=True, database_path=database_path())
        if request.method == "POST":
            try:
                activity_id = generator_service.generate_activity(request.form, user["id"], database_path())
                flash("Atividade gerada somente com os materiais selecionados.", "success")
                return redirect(url_for("activity_detail", activity_id=activity_id))
            except (ValueError, KeyError) as error:
                flash(str(error), "error")
        prompt = session.pop("creation_prompt", "")
        return render_template("generator.html", materials=materials, settings=settings, prompt=prompt)

    @app.route("/atividades/<int:activity_id>")
    @login_required
    def activity_detail(activity_id):
        activity = generator_service.get_activity(activity_id, database_path())
        if not activity:
            abort(404)
        user = current_user()
        if user["role"] == "Professor" and activity["teacher_id"] != user["id"]:
            abort(403)
        settings = standards_service.get_settings(database_path())
        return render_template("activity_detail.html", activity=activity, settings=settings)

    @app.post("/questoes/<int:question_id>/editar")
    @role_required("Professor")
    def question_edit(question_id):
        activity_id = int(request.form["activity_id"])
        try:
            generator_service.update_question(question_id, request.form, current_user()["id"], database_path())
            flash("Questão atualizada.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("activity_detail", activity_id=activity_id))

    @app.post("/questoes/<int:question_id>/excluir")
    @role_required("Professor")
    def question_delete(question_id):
        activity_id = int(request.form["activity_id"])
        generator_service.delete_question(question_id, current_user()["id"], database_path())
        flash("Questão removida.", "success")
        return redirect(url_for("activity_detail", activity_id=activity_id))

    @app.post("/questoes/<int:question_id>/trocar")
    @role_required("Professor")
    def question_regenerate(question_id):
        activity_id = int(request.form["activity_id"])
        try:
            generator_service.regenerate_question(question_id, current_user()["id"], database_path())
            flash("Questão trocada por outra baseada na mesma fonte.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("activity_detail", activity_id=activity_id))

    @app.post("/atividades/<int:activity_id>/enviar")
    @role_required("Professor")
    def activity_submit(activity_id):
        try:
            validation_service.submit_activity(activity_id, current_user()["id"], database_path())
            flash("Atividade enviada para validação institucional.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("activity_detail", activity_id=activity_id))

    @app.route("/assistente", methods=["GET", "POST"])
    @role_required("Professor")
    def assistant():
        user = current_user()
        materials = library_service.list_materials(user=user, approved_only=True, database_path=database_path())
        result = None
        if request.method == "POST":
            result = assistant_service.answer_question(
                request.form.get("question", ""), request.form.get("class_name", ""),
                request.form.get("subject", ""), user, database_path()
            )
        return render_template("assistant.html", materials=materials, result=result)

    @app.route("/verificar", methods=["GET", "POST"])
    @role_required("Professor")
    def verify_content():
        user = current_user()
        materials = library_service.list_materials(user=user, approved_only=True, database_path=database_path())
        if request.method == "POST":
            try:
                verification_id = verifier_service.verify_content(request.form, user, database_path())
                flash("Verificação concluída com rastreabilidade institucional.", "success")
                return redirect(url_for("verification_detail", verification_id=verification_id))
            except (ValueError, KeyError) as error:
                flash(str(error), "error")
        draft = session.pop("creation_prompt", "")
        return render_template("verify_form.html", materials=materials, draft=draft)

    @app.route("/verificacoes/<int:verification_id>")
    @login_required
    def verification_detail(verification_id):
        user = current_user()
        teacher_id = user["id"] if user["role"] == "Professor" else None
        verification = verifier_service.get_verification(verification_id, teacher_id, database_path())
        if not verification:
            abort(404)
        return render_template("verification_detail.html", verification=verification)

    @app.route("/validacao")
    @role_required("Coordenacao")
    def validation():
        return render_template("validation.html", activities=validation_service.pending_activities(database_path()))

    @app.post("/validacao/<int:activity_id>")
    @role_required("Coordenacao")
    def review(activity_id):
        try:
            validation_service.review_activity(
                activity_id, current_user()["id"], request.form.get("decision", ""),
                request.form.get("note", ""), database_path()
            )
            flash("Analise registrada com sucesso.", "success")
        except ValueError as error:
            flash(str(error), "error")
        return redirect(url_for("validation"))

    @app.route("/padroes", methods=["GET", "POST"])
    @role_required("Coordenacao")
    def standards():
        if request.method == "POST":
            try:
                standards_service.update_settings(request.form, database_path())
                flash("Padrões institucionais atualizados e aplicados ao gerador.", "success")
                return redirect(url_for("standards"))
            except (ValueError, KeyError) as error:
                flash(str(error), "error")
        return render_template("standards.html", settings=standards_service.get_settings(database_path()))

    @app.route("/coordenacao")
    @role_required("Coordenacao")
    def dashboard():
        return render_template("dashboard.html", dashboard=dashboard_service.get_dashboard(database_path()))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
