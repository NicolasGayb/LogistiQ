import pytest
from app.models import Produto, Usuario, db
from werkzeug.security import generate_password_hash
from sqlalchemy import text

@pytest.fixture(autouse=True)
def clean_db(app):
    """Limpa as tabelas antes de cada teste."""
    with app.app_context():
        db.session.rollback()
        # Usa text() para queries SQL puras
        db.session.execute(text('TRUNCATE TABLE atividades RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE produto RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;'))
        db.session.commit()



@pytest.fixture
def login_user(client, app):
    """Cria e faz login de um usuário para rotas protegidas."""
    with app.app_context():
        user = Usuario.query.filter_by(username="testeuser").first()
        if not user:
            user = Usuario(
                nome="Teste",
                username="testeuser",
                email="teste@mail.com",
                senha=generate_password_hash("Teste@123")
            )
            db.session.add(user)
            db.session.commit()

    # Faz login
    client.post('/login', data={"email": "teste@mail.com", "senha": "Teste@123"}, follow_redirects=True)
    return user

def test_add_product(client, app, login_user):
    response = client.post('/adicionar', data={
        "nome": "Produto Teste",
        "quantidade": 10,
        "preco": 5.5
    }, follow_redirects=True)
    
    html = response.data.decode("utf-8")
    assert "Produto adicionado com sucesso" in html
    with app.app_context():
        produto = Produto.query.filter_by(nome="Produto Teste").first()
        assert produto is not None
        assert produto.quantidade == 10
        assert produto.preco == 5.5

def test_update_product(client, app, login_user):
    p = Produto(nome="Produto Update", quantidade=1, preco=2.0)
    with app.app_context():
        db.session.add(p)
        db.session.commit()

    response = client.post(f'/atualizar/{p.id}', data={
        "quantidade": 5,
        "motivo": "Teste"
    }, follow_redirects=True)

    with app.app_context():
        produto = Produto.query.get(p.id)
        assert produto.quantidade == 5

def test_delete_product(client, app, login_user):
    p = Produto(nome="Produto Delete", quantidade=1, preco=1.0)
    with app.app_context():
        db.session.add(p)
        db.session.commit()

    response = client.get(f'/remover/{p.id}', follow_redirects=True)
    with app.app_context():
        assert Produto.query.get(p.id) is None
