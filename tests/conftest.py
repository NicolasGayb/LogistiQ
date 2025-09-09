import pytest
import uuid
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Usuario
from unittest.mock import patch

@pytest.fixture
def app():
    """Cria uma instância da aplicação configurada para testes"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,  # Desabilita CSRF para testes de formulário
    })
    with app.app_context():
        db.drop_all()
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

@pytest.fixture
def admin_user(app):
    """Cria um usuário com role 'Administrador' para testes"""
    unique_id = uuid.uuid4().hex[:6]
    username = f"testeadmin_{unique_id}"
    email = f"{username}@mail.com"

    user = Usuario(
        nome="Teste Admin",
        username=username,
        email=email,
        senha=generate_password_hash("Teste@123"),
        role="Administrador"
    )

    with app.app_context():
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture
def logged_in_client(app, client):
    """Cria um client autenticado como Administrador para testes."""
    with app.app_context():
        # Cria usuário admin
        user = Usuario(
            nome="Teste Admin",
            username="testeadmin",
            email="testeadmin@mail.com",
            senha=generate_password_hash("Teste@123"),
            role="Administrador"
        )
        db.session.add(user)
        db.session.commit()
        email, senha = user.email, "Teste@123"

    # Mock do registrar_atividade para evitar erros de NotNullViolation
    with patch("app.routes.auth_routes.registrar_atividade"):
        # Faz login sem checar flash message
        client.post(
            "/login",
            data={"email": email, "senha": senha},
            follow_redirects=True
        )

    yield client

    # Limpeza do usuário após teste
    with app.app_context():
        db.session.delete(user)
        db.session.commit()