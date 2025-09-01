import pytest
from app.models import Usuario, db
from werkzeug.security import generate_password_hash

def test_register(client, app):
    response = client.post('/registro', data={
        "nome": "Teste",
        "username": "teste123",
        "email": "teste@mail.com",
        "senha": "Teste@123",
        "confirmar_senha": "Teste@123"
    }, follow_redirects=True)
    assert 'Cadastro realizado com sucesso! Faça o login para acessar o sistema.' in response.data.decode('utf-8')

def test_login_logout(client, app):
    # Cria usuário direto no DB
    u = Usuario(
        nome="Teste",
        username="teste123",
        email="teste@mail.com",
        senha=generate_password_hash("Teste@123")
    )
    with app.app_context():
        db.session.add(u)
        db.session.commit()

    # Login
    response = client.post('/login', data={"email": "teste@mail.com", "senha": "Teste@123"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"In\xc3\xadcio" in response.data  # Verifica se a página inicial foi carregada

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
