# Inicializa o app Flask, configura extensões e registra rotas

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # <-- Importa Flask-Migrate

# Instancia as extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Define a rota padrão para login
migrate = Migrate()  # <-- Instancia o Migrate

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_segura'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:LkUWNCvpNYKUiMGgzFUiMtCBxiuSBSYI@hopper.proxy.rlwy.net:46545/railway'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # <-- Inicializa o Migrate

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