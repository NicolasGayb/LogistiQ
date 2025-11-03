import os
import sqlite3
from dotenv import load_dotenv
from app import create_app, db
from flask import render_template
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

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
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# 🔧 Inicializa extensões após configurar URI
app.init_extensions(app)

print(f"\n🔧 Ambiente: {FLASK_ENV}")
print(f"📦 Banco selecionado: {DB_NAME}")

# ======================================================
# 🔹 Testa acesso direto ao SQLite (nível SO)
# ======================================================
try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS __test__ (id INTEGER);")
    conn.close()
    print("✅ SQLite conseguiu abrir e gravar no banco com sucesso.")
except Exception as e:
    print(f"❌ Falha ao abrir o banco diretamente: {e}")

# ======================================================
# 🔹 Criação das tabelas (sem interferência do auto-reload)
# ======================================================
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    with app.app_context():
        try:
            db.engine.dispose()
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

# ======================================================
# 🔹 Executa servidor Flask
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = FLASK_ENV != "production"

    print(f"\n🚀 Servidor rodando em http://localhost:{port}/")
    print(f"🧩 Banco em uso: {DB_URI}\n")

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
