# Inicializa o app Flask, configura extensões e registra rotas

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instancia as extensões
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Define a rota padrão para login

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_segura'  # Protege sessões
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'  # Banco SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)

    # Importa modelo de usuário para o carregamento de sessões
    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registra os blueprints de rotas
    from .routes import routes as routes_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(auth_blueprint)

    return app