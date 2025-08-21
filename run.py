import os
from app import create_app, db

# Cria a aplicação
app = create_app()

# Opcional: criar tabelas localmente se estiver usando SQLite ou para teste
# NÃO recomendado para produção com PostgreSQL no Railway
if os.environ.get("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

# Roda o servidor usando a porta fornecida pelo Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
