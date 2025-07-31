# Rotas do sistema de controle de estoque

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import db
from .models import Produto

# Cria um blueprint para as rotas principais
routes = Blueprint('routes', __name__)

# Página inicial - lista de produtos
@routes.route('/')
@login_required  # Requer login
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

# Rota para adicionar um novo produto
@routes.route('/add', methods=['POST'])
@login_required
def add():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    novo_produto = Produto(nome=nome, quantidade=quantidade, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()

    flash(f'Produto "{nome}" adicionado com sucesso!')
    return redirect(url_for('routes.index'))

# Rota para atualizar a quantidade de um produto
@routes.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    produto = Produto.query.get_or_404(id)
    nova_quantidade = int(request.form['quantidade'])
    produto.quantidade = nova_quantidade
    db.session.commit()

    flash(f'Quantidade de "{produto.nome}" atualizada para {nova_quantidade}.')
    return redirect(url_for('routes.index'))

# Rota para excluir um produto
@routes.route('/delete/<int:id>')
@login_required
def delete(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()

    flash(f'Produto "{produto.nome}" removido com sucesso.')
    return redirect(url_for('routes.index'))
