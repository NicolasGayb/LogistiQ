from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import secrets

# ======================================================
# 🔹 Instância das extensões globais
# ======================================================
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
mail = Mail()
load_dotenv()


# ======================================================
# 🔹 Função de fábrica da aplicação Flask
# ======================================================
def create_app(test_config=None, instance_path=None):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    default_instance = os.path.join(base_dir, '..', 'instance')

    os.makedirs(instance_path or default_instance, exist_ok=True)
    
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates',
        instance_path=instance_path or default_instance,
        instance_relative_config=True
    )

    # --------------------------------------------------
    # 🔧 Configuração padrão do app
    # --------------------------------------------------
    secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///logistiq.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        MAIL_SERVER=os.environ.get('MAIL_SERVER'),
        MAIL_PORT=int(os.environ.get('MAIL_PORT', 587)),
        MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS', 'True') == 'True',
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
    )

    # Sobrescreve config para testes
    if test_config:
        app.config.update(test_config)

    # --------------------------------------------------
    # 🔧 Função para inicializar extensões (chamada no run.py)
    # --------------------------------------------------
    def init_extensions(app):
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)

    # 🔹 Anexa o método ao app
    app.init_extensions = init_extensions

    # --------------------------------------------------
    # 🔹 Modelo de usuário e user loader
    # --------------------------------------------------
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # --------------------------------------------------
    # 🔹 Registra blueprints
    # --------------------------------------------------
    from app.routes.web_routes import routes as routes_blueprint
    from app.routes.auth_routes import auth as auth_blueprint
    from app.routes.api_routes import api as api_blueprint
    from app.routes.admin_routes import admin_bp as admin_blueprint

    app.register_blueprint(routes_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app