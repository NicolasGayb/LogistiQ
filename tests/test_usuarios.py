import pytest
from app.models import Usuario, db
from werkzeug.security import generate_password_hash

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def admin_user(app):
    admin = Usuario(
        nome="Admin",
        username="admin",
        email="admin@test.com",
        senha=generate_password_hash("admin123", method="scrypt"),
        role="administrador",
        ativo=True
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def client_logged_in(client, admin_user):
    with client:
        client.post("/login", data={"username": "admin", "senha": "admin123"})
        yield client

# -----------------------------
# Testes da aba Usuários
# -----------------------------
def test_lista_usuarios(client_logged_in):
    response = client_logged_in.get("/admin/usuarios")
    assert response.status_code == 200
    assert "Usuários" in response.get_data(as_text=True)

def test_filtro_nome_email(client_logged_in):
    user = Usuario(
        nome="Teste Nome",
        username="testeuser",
        email="teste@email.com",
        senha=generate_password_hash("123456", method="scrypt"),
        role="usuario",
        ativo=True
    )
    db.session.add(user)
    db.session.commit()

    response = client_logged_in.get("/admin/usuarios?nome=Teste")
    assert b"Teste Nome" in response.data

    response = client_logged_in.get("/admin/usuarios?email=teste@email.com")
    assert b"Teste Nome" in response.data

def test_filtro_ativo_role(client_logged_in):
    ativo = Usuario(
        nome="Ativo User",
        username="ativo",
        email="ativo@email.com",
        senha=generate_password_hash("123456", method="scrypt"),
        role="usuario",
        ativo=True
    )
    inativo = Usuario(
        nome="Inativo User",
        username="inativo",
        email="inativo@email.com",
        senha=generate_password_hash("123456", method="scrypt"),
        role="supervisor",
        ativo=False
    )
    db.session.add_all([ativo, inativo])
    db.session.commit()

    response = client_logged_in.get("/admin/usuarios?ativo=sim")
    assert b"Ativo User" in response.data
    assert b"Inativo User" not in response.data

    response = client_logged_in.get("/admin/usuarios?ativo=nao")
    assert b"Inativo User" in response.data
    assert b"Ativo User" not in response.data

    response = client_logged_in.get("/admin/usuarios?role=supervisor")
    assert b"Inativo User" in response.data
    assert b"Ativo User" not in response.data

def test_criar_usuario_sucesso(client_logged_in):
    response = client_logged_in.post(
        "/admin/usuarios/criar",
        data={
            "nome": "Novo Usuário",
            "username": "novouser",
            "email": "novo@email.com",
            "senha": "senha123",
            "role": "usuario",
            "ativo": "1"
        },
        follow_redirects=True
    )
    assert b"Usuário criado com sucesso" in response.data
    assert Usuario.query.filter_by(username="novouser").first() is not None

def test_criar_usuario_erro(client_logged_in):
    # Campos obrigatórios faltando
    response = client_logged_in.post(
        "/admin/usuarios/criar",
        data={
            "nome": "",
            "username": "",
            "email": "",
            "senha": "",
            "role": ""
        },
        follow_redirects=True
    )
    assert b"Preencha todos os campos obrigatórios" in response.data

    # Duplicidade
    response = client_logged_in.post(
        "/admin/usuarios/criar",
        data={
            "nome": "Admin",
            "username": "admin",
            "email": "admin@test.com",
            "senha": "admin123",
            "role": "administrador",
            "ativo": "1"
        },
        follow_redirects=True
    )
    assert b"Já existe um usuário com esse username ou email" in response.data

def test_editar_usuario_sucesso(client_logged_in):
    user = Usuario.query.filter_by(username="admin").first()
    response = client_logged_in.post(
        f"/admin/usuarios/editar/{user.id}",
        data={
            "nome": "Admin Editado",
            "username": "admin",
            "email": "admin@test.com",
            "role": "administrador",
            "ativo": "1"
        },
        follow_redirects=True
    )
    assert b"Usuário atualizado com sucesso" in response.data
    user_db = Usuario.query.get(user.id)
    assert user_db.nome == "Admin Editado"

def test_editar_usuario_erro(client_logged_in):
    user = Usuario.query.filter_by(username="admin").first()
    response = client_logged_in.post(
        f"/admin/usuarios/editar/{user.id}",
        data={
            "nome": "",
            "username": "",
            "email": "",
            "role": ""
        },
        follow_redirects=True
    )
    assert b"Preencha todos os campos obrigatórios" in response.data

def test_excluir_usuario(client_logged_in):
    user = Usuario(
        nome="Excluir User",
        username="excluir",
        email="excluir@email.com",
        senha=generate_password_hash("123456", method="scrypt"),
        role="usuario",
        ativo=True
    )
    db.session.add(user)
    db.session.commit()

    response = client_logged_in.post(
        f"/admin/usuarios/excluir/{user.id}",
        follow_redirects=True
    )
    assert b"Usuário excluído com sucesso" in response.data
    assert Usuario.query.get(user.id) is None
