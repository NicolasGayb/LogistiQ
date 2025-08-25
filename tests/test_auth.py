def test_register(client):
    response = client.post('/register', data={
        "nome": "Teste",
        "username": "teste123",
        "email": "teste@mail.com",
        "senha": "123456",
        "confirmar_senha": "123456"
    }, follow_redirects=True)
    assert b"Cadastro realizado com sucesso" in response.data

def test_login_logout(client, app):
    # Cria usuário direto no DB
    from app.models import Usuario
    u = Usuario(nome="Teste", username="teste123", email="teste@mail.com")
    u.set_password("123456")
    db.session.add(u)
    db.session.commit()

    # Login
    response = client.post('/login', data={"username": "teste123", "senha": "123456"}, follow_redirects=True)
    assert b"Bem-vindo" in response.data

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data
