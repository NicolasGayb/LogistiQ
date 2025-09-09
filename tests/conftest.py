import pytest
import uuid
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Usuario
from unittest.mock import patch

@pytest.fixture
def app():
    """Cria a app configurada para testes"""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
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
    """Cliente autenticado como Administrador"""
    with app.app_context():
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

    # Mock do registrar_atividade
    with patch("app.routes.auth_routes.registrar_atividade"):
        client.post(
            "/login",
            data={"email": email, "senha": senha},
            follow_redirects=True
        )

    yield client

    with app.app_context():
        db.session.delete(user)
        db.session.commit()
