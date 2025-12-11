import os
import sqlite3
from dotenv import load_dotenv
from app import create_app, db
from flask import render_template, jsonify, request
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from app.models import Usuario
from werkzeug.security import generate_password_hash

# ======================================================
# 🔹 Configura ambiente e Sentry
# ======================================================
load_dotenv()
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# ======================================================
# 🔹 Define caminhos fixos
# ======================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_PATH, exist_ok=True)

FLASK_ENV = os.getenv("FLASK_ENV", "development").lower()
IS_TESTING = "test" in FLASK_ENV or os.getenv("DATABASE_MODE") == "test"
DB_NAME = "test_logistiq.db" if IS_TESTING else "logistiq.db"

DB_PATH = os.path.join(INSTANCE_PATH, DB_NAME).replace("\\", "/")
DB_URI = f"sqlite:///{DB_PATH}"  # caminho absoluto no formato correto

# ======================================================
# 🔹 Cria app e aplica configuração definitiva
# ======================================================
app = create_app(instance_path=INSTANCE_PATH)
app.config.update(
    SQLALCHEMY_DATABASE_URI=DB_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    TESTING=IS_TESTING
)

print(f"\n🔧 Ambiente: {FLASK_ENV}")
print(f"📦 Banco selecionado: {DB_NAME}")

# ======================================================
# 🔹 (Opcional) Testa acesso direto ao SQLite
# ======================================================
try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS __test__ (id INTEGER);")
    conn.close()
    print("✅ SQLite conseguiu abrir e gravar no banco com sucesso.")
except Exception as e:
    print(f"❌ Falha ao abrir o banco diretamente: {e}")

# ======================================================
# 🔹 Criação das tabelas
#    - Em teste: garante drop_all + create_all na subida
#    - Fora de teste: apenas create_all (ou usa migrações)
# ======================================================
with app.app_context():
    try:
        if IS_TESTING:
            db.session.remove()
            db.drop_all()
        db.create_all()
        print(f"✅ Banco inicializado: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

# ======================================================
# 🔹 Handler para erro 403
# ======================================================
@app.errorhandler(403)
def forbidden(e):
    return render_template('acesso_negado.html'), 403

# ============================================================
# 🔹 ROTA PARA RESETAR O BANCO DE TESTES (usada pelo Cypress)
# ============================================================
@app.route("/api/test/reset_db", methods=["POST"])
def reset_db():
    """Apaga e recria todas as tabelas (modo de teste)."""
    if not app.config.get("TESTING", False):
        return jsonify({"error": "Operação permitida apenas em ambiente de teste."}), 403

    try:
        print("🧩 Resetando banco de teste via drop_all/create_all...")
        db.session.remove()
        db.drop_all()
        db.create_all()

        # 🔹 cria o admin usado no Cypress
        admin = Usuario(
            nome="Teste Cypress",
            username="TesteCypress",
            email="teste@example.com",
            senha=generate_password_hash("senha_teste"),
            role="administrador",
            ativo=True,
        )
        # 🔹 cria o supervisor usado no Cypress
        supervisor = Usuario(
            nome="Supervisor Cypress",
            username="SupervisorCypress",
            email="supervisor@example.com",
            senha=generate_password_hash("senha_teste"),
            role="supervisor",
            ativo=True,
        )
        # cria o usuário comum usado no Cypress
        usuario = Usuario(
            nome="Usuário Cypress",
            username="UsuarioCypress",
            email="usuario@example.com",
            senha=generate_password_hash("senha_teste"),
            role="usuario",
            ativo=True,
        )
        # cria o usuário convidado usado no Cypress
        usuario_convidado = Usuario(
            nome="Usuário Convidado Cypress",
            username="UsuarioConvidadoCypress",
            email="convidado@example.com",
            senha=generate_password_hash("senha_teste"),
            role="convidado",
            ativo=True,
        )

        # cria o usuário inativo usado no Cypress
        usuario_inativo = Usuario(
            nome="Usuário Inativo Cypress",
            username="UsuarioInativoCypress",
            email="inativo@example.com",
            senha=generate_password_hash("senha_teste"),
            role="usuario",
            ativo=False,
        )

        db.session.add(usuario_inativo)
        db.session.add(usuario_convidado)
        db.session.add(usuario)
        db.session.add(supervisor)
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "Banco de testes recriado com sucesso."}), 200

    except Exception as e:
        print(f"❌ Erro ao resetar banco de teste: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================
# 🔹 ROTA PARA PROMOVER UM USUÁRIO A ADMIN (usada pelo Cypress)
# ============================================================
@app.route("/api/test/promote_admin", methods=["POST"])
def promote_admin():
    """Define o usuário informado como administrador."""
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "E-mail é obrigatório"}), 400

    try:
        user = Usuario.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        user.role = "administrador"
        db.session.commit()
        return jsonify({"message": f"Usuário {email} promovido a administrador."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ======================================================
# 🔹 Executa servidor Flask
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    # Em CI/teste não queremos debug nem reloader
    if IS_TESTING:
        debug_mode = False
    else:
        debug_mode = FLASK_ENV != "production"

    print(f"\n🚀 Servidor rodando em http://localhost:{port}/")
    print(f"🧩 Banco em uso: {DB_URI}\n")

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
