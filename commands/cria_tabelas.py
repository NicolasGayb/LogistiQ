
from app import db, create_app

def criar_tabelas():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Tabelas criadas com sucesso!')

if __name__ == '__main__':
    criar_tabelas()