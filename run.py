from app import create_app, db

app = create_app()

# Cria o banco se não existir (SQLite local)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
