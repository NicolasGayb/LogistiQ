import pytest
from app import create_app, db
from app.models import Usuario, Produto
from werkzeug.security import generate_password_hash
from flask_login import login_user

@pytest.fixture
def app_instance():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def logged_in_client(app_instance):
    """Cria um client autenticado com role correta."""
    client = app_instance.test_client()

    with app_instance.app_context():
        # Cria usuário admin com role em minúsculo
        admin_user = Usuario(
            nome="Teste Admin",
            username="testeadmin",
            email="testeadmin@mail.com",
            senha=generate_password_hash("Teste@123"),
            role="administrador"  # deve bater com @role_required
        )
        db.session.add(admin_user)
        db.session.commit()
        admin_id = admin_user.id

    # Força login dentro de um request context
    with client:
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_id)
        yield client


def test_add_product(logged_in_client, app_instance):
    """Testa adicionar produto via POST."""
    client = logged_in_client

    # Adiciona produto
    response = client.post(
        "/adicionar",
        data={"nome": "Produto Teste", "quantidade": 10, "preco": 5.5},
        follow_redirects=True
    )
    assert response.status_code == 200

    # Verifica se produto foi adicionado no banco
    with app_instance.app_context():
        produto = Produto.query.filter_by(nome="Produto Teste").first()
        assert produto is not None
        assert produto.quantidade == 10
        assert produto.preco == 5.5


def test_update_product(logged_in_client, app_instance):
    """Testa atualizar quantidade de um produto."""
    client = logged_in_client

    with app_instance.app_context():
        produto = Produto(nome="Produto Update", quantidade=5, preco=2.5)
        db.session.add(produto)
        db.session.commit()
        produto_id = produto.id

    # Atualiza produto
    response = client.post(
        f"/atualizar/{produto_id}",
        data={"quantidade": 15, "motivo": "Teste update"},
        follow_redirects=True
    )
    assert response.status_code == 200

    with app_instance.app_context():
        produto = Produto.query.get(produto_id)
        assert produto.quantidade == 15

def test_remove_product(logged_in_client, app_instance):
    """Testa remover produto do estoque."""
    client = logged_in_client

    with app_instance.app_context():
        produto = Produto(nome="Produto Remove", quantidade=3, preco=1.5)
        db.session.add(produto)
        db.session.commit()
        produto_id = produto.id

    # Remove produto
    response = client.get(f"/remover/{produto_id}", follow_redirects=True)
    assert response.status_code == 200

    with app_instance.app_context():
        produto = Produto.query.get(produto_id)
        assert produto is None
