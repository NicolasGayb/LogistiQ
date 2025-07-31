from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  # Chave secreta para sessões

login_manager = LoginManager()
login_manager.login_view = 'login'  # redireciona para a rota 'login' se não estiver autenticado
login_manager.init_app(app)

# Configura o banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para o produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Modelo para o usuário (para autenticação)
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
@login_required  # Protege a rota, exigindo que o usuário esteja autenticado
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            flash('Login realizado com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha inválidos.')
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta.')
    return redirect(url_for('login'))

# Validação da senha
def senha_valida(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos um número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return "A senha deve conter pelo menos um caractere especial."
    return None  # senha válida

# Rota para registrar um novo usuário
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        erro = senha_valida(senha)
        if erro:
            flash(erro)
            return redirect(url_for('registro'))

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('E-mail já cadastrado.')
            return redirect(url_for('registro'))

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha)
        )
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça o login.')
        return redirect(url_for('login'))

    return render_template('registro.html')

# Rota para adicionar um novo produto
@app.route('/add', methods=['POST'])
@login_required  # Protege a rota, exigindo que o usuário esteja autenticado
def add():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    novo_produto = Produto(nome=nome, quantidade=quantidade, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()

    flash(f'Produto "{nome}" adicionado com sucesso!')
    return redirect(url_for('index'))

# Rota para editar um produto existente
@app.route('/update/<int:id>', methods=['POST'])
@login_required  # Protege a rota, exigindo que o usuário esteja autenticado
def update(id):
    produto = Produto.query.get_or_404(id)
    produto.quantidade = int(request.form['quantidade'])
    db.session.commit()

    flash(f'Quantidade do produto "{produto.nome}" atualizada para {produto.quantidade}.')
    return redirect(url_for('index'))

# Rota para excluir um produto
@app.route('/delete/<int:id>')
@login_required  # Protege a rota, exigindo que o usuário esteja autenticado
def delete(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()

    flash(f'Produto "{produto.nome}" removido com sucesso!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

