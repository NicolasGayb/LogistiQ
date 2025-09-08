import pytest
from app import create_app, db
from app.models import Usuario
from flask_login import login_user, logout_user
from datetime import datetime, timezone

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # banco em memória para testes
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def create_user():
    def _create_user(email, role, senha="Teste@123"):
        user = Usuario(
            nome="Teste",
            username=email.split("@")[0],  # preenchendo username para evitar NOT NULL
            email=email,
            senha=senha,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user

def login(client, email, senha="Teste@123"):
    return client.post(
        "/login",
        data={"email": email, "senha": senha},
        follow_redirects=True
    )

# -------------------------------
# TESTES
# -------------------------------

# Função auxiliar para forçar login via session
def login_via_session(client, user):
    with client.session_transaction() as sess:
        sess['_user_id'] = str(user.id)
        sess['_fresh'] = True


def test_historico_acesso_administrador(client, create_user):
    logged_in_client = create_user("admin@test.com", "administrador")
    login_via_session(client, logged_in_client)

    response = client.get("/historico", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Histórico" in html


def test_historico_acesso_supervisor(client, create_user):
    supervisor_user = create_user("super@test.com", "supervisor")
    login_via_session(client, supervisor_user)

    response = client.get("/historico", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Histórico" in html


def test_historico_bloqueio_usuario(client, create_user):
    usuario = create_user("usuario@test.com", "usuario")
    login_via_session(client, usuario)

    response = client.get("/historico", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Acesso negado" in html