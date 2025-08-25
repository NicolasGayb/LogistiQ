from app.models import Produto, db

def test_add_product(client, app):
    response = client.post('/adicionar_produto', data={
        "nome": "Produto Teste",
        "quantidade": 10,
        "preco": 5.5
    }, follow_redirects=True)
    assert b"Produto adicionado com sucesso" in response.data
    assert Produto.query.filter_by(nome="Produto Teste").first() is not None

def test_update_product(client, app):
    p = Produto(nome="Produto Update", quantidade=1, preco=2.0)
    db.session.add(p)
    db.session.commit()

    response = client.post(f'/atualizar_produto/{p.id}', data={
        "quantidade": 5,
        "motivo": "Teste"
    }, follow_redirects=True)
    p = Produto.query.get(p.id)
    assert p.quantidade == 5

def test_delete_product(client, app):
    p = Produto(nome="Produto Delete", quantidade=1, preco=1.0)
    db.session.add(p)
    db.session.commit()

    response = client.get(f'/remover_produto/{p.id}', follow_redirects=True)
    assert Produto.query.get(p.id) is None
