import os
from app import create_app, db

# Cria a aplicação
app = create_app()

port = int(os.environ.get("PORT", 5000))

# Cria as tabelas do banco de dados se não existirem
with app.app_context():
    db.create_all() # Garante que as tabelas sejam criadas no banco de dados
    print("Banco de dados inicializado.")

# Roda o servidor usando a porta fornecida pelo Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)



