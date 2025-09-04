# Inicializa o app Flask, configura extensões e registra rotas

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # <-- Importa Flask-Migrate
from dotenv import load_dotenv
import os
import secrets

# Instancia as extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Define a rota padrão para login
migrate = Migrate()
mail = Mail()  # <-- Agora o mail é global, fora da função
load_dotenv()

def create_app():
    app = Flask(__name__)
    secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.secret_key = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LkUWNCvpNYKUiMGgzFUiMtCBxiuSBSYI@hopper.proxy.rlwy.net:46545/railway'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração do e-mail
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    
    # Configuração JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Inicializa as extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Importa modelo de usuário para o carregamento de sessões
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registra os blueprints de rotas
    from app.routes.web_routes import routes as routes_blueprint
    from app.routes.auth_routes import auth as auth_blueprint
    from app.routes.api_routes import api as api_blueprint

    app.register_blueprint(routes_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
