import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Cria uma instância da aplicação configurada para testes"""
    app = create_app(test_config=None, testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste que pode fazer requisições HTTP"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner para executar comandos CLI do Flask"""
    return app.test_cli_runner()
