import pytest
from app.models import HistoricoMovimentacao, Usuario, db
from werkzeug.security import generate_password_hash
from datetime import datetime
import uuid

def test_historico_record(client, app):
    # Gera dados únicos para evitar conflito de chave única
    unique_id = uuid.uuid4().hex[:6]
    username = f"testeuser_{unique_id}"
    email = f"{username}@mail.com"

    # Cria usuário para relação
    u = Usuario(
        nome="Teste",
        username=username,
        email=email,
        senha=generate_password_hash("Teste@123")
    )

    with app.app_context():
        # Salva o usuário no DB
        db.session.add(u)
        db.session.commit()

        # Cria histórico vinculado ao usuário
        h = HistoricoMovimentacao(
            produto_id=1,
            produto_nome="Produto Exemplo",
            usuario=u.nome,
            acao="Cadastro de produto",
            quantidade_anterior=0,
            quantidade_nova=10,
            motivo="Teste de criação",
            data_hora=datetime.utcnow()
        )
        db.session.add(h)
        db.session.commit()

    # Faz login do usuário antes de acessar rota protegida
    client.post('/login', data={"email": email, "senha": "Teste@123"}, follow_redirects=True)

    # Agora acessa a rota /historico
    response = client.get('/historico', follow_redirects=True)
    assert response.status_code == 200
    assert b"Cadastro de produto" in response.data
    assert b"Produto Exemplo" in response.data