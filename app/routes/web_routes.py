from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Produto, HistoricoMovimentacao
from datetime import datetime

routes = Blueprint('routes', __name__)

# ------------------------
# ROTA PRINCIPAL - ESTOQUE
# ------------------------
@routes.route('/')
@login_required
def index():
    produtos = Produto.query.all()
    valor_total_estoque = sum(p.quantidade * p.preco for p in produtos)

    # Preparar dados para gráficos ou JS
    estoque_labels = [p.nome for p in produtos]
    estoque_quantidades = [p.quantidade for p in produtos]
    estoque_valores = [p.quantidade * p.preco for p in produtos]

    return render_template(
        'index.html', 
        produtos=produtos, 
        usuario=current_user, 
        valor_total_estoque=valor_total_estoque,
        estoque_labels=estoque_labels,
        estoque_quantidades=estoque_quantidades,
        estoque_valores=estoque_valores
    )

# ------------------------
# ADICIONAR PRODUTO
# ------------------------
@routes.route('/adicionar', methods=['POST'])
@login_required
def adicionar_produto():
    nome = request.form.get('nome')
    quantidade = int(request.form.get('quantidade'))
    preco = float(request.form.get('preco'))

    novo_produto = Produto(nome=nome, quantidade=quantidade, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()  # Commit para gerar o ID do produto

    # Registrar no histórico
    historico = HistoricoMovimentacao(
        produto_id=novo_produto.id,
        usuario=current_user.username,
        acao='Adicionar',
        quantidade_anterior=None,
        quantidade_nova=quantidade,
        motivo='Novo produto adicionado'
    )
    db.session.add(historico)
    db.session.commit()

    flash(f'Produto "{nome}" adicionado com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# ATUALIZAR PRODUTO
# ------------------------
@routes.route('/atualizar/<int:id>', methods=['POST'])
@login_required
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)

    quantidade_anterior = produto.quantidade
    quantidade_nova = int(request.form.get('quantidade'))
    motivo = request.form.get('motivo')

    produto.quantidade = quantidade_nova
    db.session.commit()

    # Registrar no histórico
    historico = HistoricoMovimentacao(
        produto_id=produto.id,
        usuario=current_user.username,
        acao='Atualizar',
        quantidade_anterior=quantidade_anterior,
        quantidade_nova=quantidade_nova,
        motivo=motivo
    )
    db.session.add(historico)
    db.session.commit()

    flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# REMOVER PRODUTO
# ------------------------
@routes.route('/remover/<int:id>')
@login_required
def remover_produto(id):
    produto = Produto.query.get_or_404(id)

    # Registrar no histórico ANTES de deletar
    historico = HistoricoMovimentacao(
        produto_id=produto.id,
        usuario=current_user.username,
        acao='Remover',
        quantidade_anterior=produto.quantidade,
        quantidade_nova=0,
        motivo='Produto removido do estoque'
    )
    db.session.add(historico)
    db.session.commit()  # Garante que o histórico esteja registrado na session antes de deletar

    db.session.delete(produto)
    db.session.commit()

    flash(f'Produto "{produto.nome}" removido com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# HISTÓRICO DE MOVIMENTAÇÕES
# ------------------------
@routes.route('/historico')
@login_required
def historico():
    # Ordena por data/hora decrescente
    historico = HistoricoMovimentacao.query.order_by(HistoricoMovimentacao.data_hora.desc()).all()

    # Ajusta para casos em que o produto foi deletado
    for h in historico:
        if h.produto is None:
            h.produto_nome = 'Produto removido'
        else:
            h.produto_nome = h.produto.nome

    return render_template(
        'historico.html',
        historico=historico,
        agora=datetime.now()
    )

