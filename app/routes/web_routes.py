from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Produto, HistoricoMovimentacao, Atividade, Usuario
from app.utils import registrar_atividade, listar_atividades
from datetime import datetime
import pytz
from app.decorators import role_required    

routes = Blueprint('routes', __name__)
utc = pytz.utc
brt = pytz.timezone('America/Sao_Paulo')

# ------------------------
# ROTA PRINCIPAL - ESTOQUE
# ------------------------
@routes.route('/')
@login_required
def index():
    produtos = Produto.query.all()
    valor_total_estoque = sum(p.quantidade * p.preco for p in produtos)

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
@role_required('administrador', 'usuario_padrao', 'supervisor') 
def adicionar_produto():
    nome = request.form.get('nome')
    quantidade = int(request.form.get('quantidade'))
    preco = float(request.form.get('preco'))

    novo_produto = Produto(nome=nome, quantidade=quantidade, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()  # gera ID

    agora_utc = datetime.now(utc)
    novo_historico = HistoricoMovimentacao(
        produto_id=novo_produto.id,
        produto_nome=novo_produto.nome,
        usuario=current_user.nome,
        acao="Adicionar",
        quantidade_anterior=None,
        quantidade_nova=novo_produto.quantidade,
        motivo="Novo produto adicionado",
        data_hora=agora_utc
    )
    db.session.add(novo_historico)
    db.session.commit()

    registrar_atividade(current_user, f"Adicionou o produto '{novo_produto.nome}' ao estoque")

    flash(f'Produto "{nome}" adicionado com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# ATUALIZAR PRODUTO
# ------------------------
@routes.route('/atualizar/<int:id>', methods=['POST'])
@login_required
@role_required('administrador', 'usuario_padrao', 'supervisor')  # Admin, Usuário padrão e Supervisor
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    quantidade_anterior = produto.quantidade
    quantidade_nova = int(request.form.get('quantidade'))
    motivo = request.form.get('motivo')

    produto.quantidade = quantidade_nova
    db.session.commit()

    agora_utc = datetime.now(utc)
    historico = HistoricoMovimentacao(
        produto_id=produto.id,
        produto_nome=produto.nome,
        usuario=current_user.username,
        acao='Atualizar',
        quantidade_anterior=quantidade_anterior,
        quantidade_nova=quantidade_nova,
        motivo=motivo,
        data_hora=agora_utc
    )
    db.session.add(historico)
    db.session.commit()

    registrar_atividade(current_user, f"Atualizou o produto '{produto.nome}'")

    flash(f'Produto "{produto.nome}" atualizado com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# REMOVER PRODUTO
# ------------------------
@routes.route('/remover/<int:id>')
@login_required
@role_required('administrador', 'supervisor')  # Apenas Admin e Supervisor podem remover
def remover_produto(id):
    produto = Produto.query.get_or_404(id)

    agora_utc = datetime.now(utc)
    historico = HistoricoMovimentacao(
        produto_id=produto.id,
        produto_nome=produto.nome,
        usuario=current_user.username,
        acao='Remover',
        quantidade_anterior=produto.quantidade,
        quantidade_nova=0,
        motivo='Produto removido do estoque',
        data_hora=agora_utc
    )

    db.session.add(historico)
    db.session.commit()
    db.session.delete(produto)
    db.session.commit()

    registrar_atividade(current_user, f"Removeu o produto '{produto.nome}' do estoque")

    flash(f'Produto "{produto.nome}" removido com sucesso!', 'success')
    return redirect(url_for('routes.index'))

# ------------------------
# HISTÓRICO DE MOVIMENTAÇÕES
# ------------------------
@routes.route('/historico')
@login_required
@role_required('administrador', 'supervisor')  # Apenas Admin e Supervisor podem ver histórico completo
def historico():
    ordenar_por = request.args.get('ordenar', 'data')
    ordem = request.args.get('ordem', 'desc')

    campo = HistoricoMovimentacao.acao if ordenar_por == 'acao' else HistoricoMovimentacao.data_hora
    historico = (HistoricoMovimentacao.query.order_by(campo.asc() if ordem=='asc' else campo.desc()).all())

    for h in historico:
        h.data_hora = h.data_hora.replace(tzinfo=utc).astimezone(brt)

    agora = datetime.now(utc).astimezone(brt)
    return render_template('historico.html', historico=historico, agora=agora,
                           ordenar_por=ordenar_por, ordem=ordem)

# ------------------------
# PERFIL DO USUÁRIO
# ------------------------
@routes.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        # Email não pode ser alterado
        senha = request.form.get('senha')  # opcional

        current_user.nome = nome
        if senha:
            current_user.set_password(senha)
        db.session.commit()

        flash('Informações do perfil atualizadas com sucesso!', 'success')
        return redirect(url_for('routes.perfil'))

    atividades = Atividade.query.filter_by(usuario_id=current_user.id).order_by(Atividade.data.desc()).all()
    return render_template('perfil.html', usuario=current_user, atividades=atividades)

# ------------------------
# Relatório
# ------------------------
@routes.route('/relatorio')
@login_required
@role_required('administrador', 'supervisor')  # Apenas Admin e Supervisor podem ver relatório
def relatorio():
    produtos = Produto.query.all()
    valor_total_estoque = sum(p.quantidade * p.preco for p in produtos)

    estoque_labels = [p.nome for p in produtos]
    estoque_quantidades = [p.quantidade for p in produtos]
    estoque_valores = [p.quantidade * p.preco for p in produtos]

    return render_template(
        'relatorio.html', 
        produtos=produtos, 
        usuario=current_user, 
        valor_total_estoque=valor_total_estoque,
        estoque_labels=estoque_labels,
        estoque_quantidades=estoque_quantidades,
        estoque_valores=estoque_valores
    )

# ------------------------

# Página para acesso negado
@routes.route('/acesso_negado')
def acesso_negado():
    return render_template('acesso_negado.html'), 403
# ------------------------

# DARK MODE TOGGLE
@routes.route('/toggle_theme', methods=['POST'])
@login_required
def toggle_theme():
    current_user.tema_escuro = 'tema_escuro' in request.form
    db.session.commit()

    flash('Preferência de tema atualizada!', 'success')
    return redirect(url_for('routes.perfil'))
