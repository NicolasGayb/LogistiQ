from app.models import HistoricoMovimentacao, db

def test_historico_record(client, app):
    # Adiciona histórico manual
    h = HistoricoMovimentacao(acao="Teste", usuario_id=1)
    db.session.add(h)
    db.session.commit()

    response = client.get('/historico')
    assert b"Teste" in response.data
