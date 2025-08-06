from app import create_app

# Cria a aplicação Flask com base na função de fábrica em __init__.py
app = create_app()

# Executa a aplicação no modo de desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)
