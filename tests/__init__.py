from flask import Flask
from app.models import db

def create_app(test_config=None, testing=True):
    app = Flask(__name__)

    # Configuração padrão
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logistiq.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecret'

    # Se estiver rodando testes
    if testing:
        app.config.from_object("config.TestingConfig")
    elif test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object("config.DevelopmentConfig")

    return app

    # Inicializa o banco
    db.init_app(app)

    # Registro de rotas mínimas (pode mover para um blueprint depois)
    @app.route('/')
    def home():
        return "LogistiQ rodando!"

    return app
