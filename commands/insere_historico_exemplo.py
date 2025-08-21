from app import db, create_app
from app.models import EstoqueHistorico
from datetime import date, timedelta

app = create_app()

with app.app_context():
    # Insere 7 dias de histórico de exemplo
    hoje = date.today()
    for i in range(7):
        dia = hoje - timedelta(days=6-i)
        valor = 1000 + i * 100  # Exemplo: valor crescente
        if not EstoqueHistorico.query.filter_by(data=dia).first():
            registro = EstoqueHistorico(data=dia, valor_total=valor)
            db.session.add(registro)
    db.session.commit()
    print('Registros de exemplo inseridos!')
