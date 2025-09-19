from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import secrets

# Instância das extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
mail = Mail()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    # Config padrão
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

    # Inicializa extensões após config final
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Modelo de usuário
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Registra blueprints
    from app.routes.web_routes import routes as routes_blueprint
    from app.routes.auth_routes import auth as auth_blueprint
    from app.routes.api_routes import api as api_blueprint
    from app.routes.admin_routes import admin_bp as admin_blueprint

    app.register_blueprint(routes_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return app
