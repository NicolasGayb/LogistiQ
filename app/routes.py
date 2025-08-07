
# Rotas do sistema de controle de estoque
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import db
from .models import Produto

# Cria um blueprint para as rotas principais
routes = Blueprint('routes', __name__)

# Rota para histórico de movimentações
@routes.route('/historico')
@login_required
def historico():
    from .models import Movimentacao, Produto, Usuario
    movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).all()
    # Resolve os relacionamentos manualmente se não houver backref
    for mov in movimentacoes:
        mov.produto = Produto.query.get(mov.produto_id)
        mov.usuario = Usuario.query.get(mov.usuario_id)
    return render_template('historico.html', movimentacoes=movimentacoes)

# Página inicial - lista de produtos
@routes.route('/')
@login_required  # Requer login
def index():
    from datetime import date
    from .models import EstoqueHistorico
    produtos = Produto.query.all()
    valor_total_estoque = sum(p.quantidade * p.preco for p in produtos)

    # Salva o valor do estoque no histórico do dia, se ainda não registrado
    hoje = date.today()
    historico_hoje = EstoqueHistorico.query.filter_by(data=hoje).first()
    if not historico_hoje:
        novo_historico = EstoqueHistorico(data=hoje, valor_total=valor_total_estoque)
        db.session.add(novo_historico)
        db.session.commit()

    # Busca os dados para o gráfico
    historico = EstoqueHistorico.query.order_by(EstoqueHistorico.data.asc()).all()
    estoque_labels = [h.data.strftime('%d/%m') for h in historico]
    estoque_valores = [h.valor_total for h in historico]

    return render_template(
        'index.html',
        produtos=produtos,
        valor_total_estoque=valor_total_estoque,
        estoque_labels=estoque_labels,
        estoque_valores=estoque_valores
    )

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
    from flask_login import current_user
    from datetime import datetime
    from .models import Movimentacao

    produto = Produto.query.get_or_404(id)
    nova_quantidade = int(request.form['quantidade'])
    motivo = request.form.get('motivo', '')
    quantidade_anterior = produto.quantidade

    # Atualiza quantidade
    produto.quantidade = nova_quantidade
    db.session.commit()

    # Registra movimentação
    movimentacao = Movimentacao(
        produto_id=produto.id,
        usuario_id=current_user.id,
        data=datetime.now(),
        quantidade_anterior=quantidade_anterior,
        quantidade_nova=nova_quantidade,
        motivo=motivo
    )
    db.session.add(movimentacao)
    db.session.commit()

    flash(f'Quantidade de "{produto.nome}" atualizada para {nova_quantidade}. Motivo: {motivo}')
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
