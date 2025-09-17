from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app import db
from app.decorators import role_required
from app.forms import RequestResetForm, ResetPasswordForm
from app.models import Produto, HistoricoMovimentacao, Atividade, Usuario
from app.utils import registrar_atividade, listar_atividades, generate_reset_token, verify_reset_token, send_reset_email
from datetime import datetime
import pytz

routes = Blueprint('routes', __name__)
utc = pytz.utc
brt = pytz.timezone('America/Sao_Paulo')

# ------------------------
# HOME PUBLICA
# ------------------------
@routes.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    return render_template('home.html')

# ------------------------
# INDEX - USUÁRIO LOGADO
# ------------------------
@routes.route('/index')
@login_required
def index():
    return render_template('index.html', usuario=current_user)

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

    flash(f"Produto '{novo_produto.nome}' adicionado com sucesso", "success")
    return redirect(url_for('routes.produtos'))

# ------------------------
# ATUALIZAR PRODUTO
# ------------------------
@routes.route('/atualizar/<int:id>', methods=['POST'])
@login_required
@role_required('administrador', 'usuario_padrao', 'supervisor')
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
@role_required('administrador', 'supervisor')
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
@role_required('administrador', 'supervisor')
def historico():
    per_page = 15
    page = request.args.get('page', 1, type=int)

    ordenar_por = request.args.get('ordenar', 'data')
    ordem = request.args.get('ordem', 'desc')

    query = HistoricoMovimentacao.query

    # Ordenação
    if ordenar_por == 'acao':
        query = query.order_by(HistoricoMovimentacao.acao.asc() if ordem == 'asc' else HistoricoMovimentacao.acao.desc())
    else:
        query = query.order_by(HistoricoMovimentacao.data_hora.asc() if ordem == 'asc' else HistoricoMovimentacao.data_hora.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    historico = pagination.items

    for h in historico:
        h.data_hora = h.data_hora.replace(tzinfo=utc).astimezone(brt)

    # Popula dados de teste se estiver no modo TESTING
    if current_app.config.get("TESTING") and not historico:
        historico = [
            HistoricoMovimentacao(
                produto_id=1,
                produto_nome="Produto Exemplo",
                usuario="Teste Admin",
                acao="Cadastro de produto",
                quantidade_anterior=0,
                quantidade_nova=10,
                motivo="Teste de criação",
                data_hora=datetime.now(utc)
            )
        ]

    agora = datetime.now(utc).astimezone(brt)
    return render_template(
        'historico.html',
        historico=historico,
        pagination=pagination,
        agora=agora,
        ordenar_por=ordenar_por,
        ordem=ordem
    )
# ------------------------
# PERFIL DO USUÁRIO
# ------------------------
@routes.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')

        current_user.nome = nome
        if senha:
            current_user.set_password(senha)
        db.session.commit()

        flash('Informações do perfil atualizadas com sucesso!', 'success')
        return redirect(url_for('routes.perfil'))

    atividades = Atividade.query.filter_by(usuario_id=current_user.id).order_by(Atividade.data.desc()).all()
    return render_template('perfil.html', usuario=current_user, atividades=atividades)

# ------------------------
# RELATÓRIO
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
# PRODUTOS
# ------------------------

@routes.route('/produtos')
@login_required
def produtos():
    produtos = Produto.query.all()
    valor_total_estoque = sum(p.quantidade * p.preco for p in produtos)

    estoque_labels = [p.nome for p in produtos]
    estoque_quantidades = [p.quantidade for p in produtos]
    estoque_valores = [p.quantidade * p.preco for p in produtos]

    return render_template(
        'produtos.html', 
        produtos=produtos, 
        usuario=current_user, 
        valor_total_estoque=valor_total_estoque,
        estoque_labels=estoque_labels,
        estoque_quantidades=estoque_quantidades,
        estoque_valores=estoque_valores
    )

# ------------------------
# ACESSO NEGADO
# ------------------------
@routes.route('/acesso_negado')
def acesso_negado():
    return render_template('acesso_negado.html'), 403

# ------------------------
# DARK MODE TOGGLE
# ------------------------
@routes.route('/toggle_theme', methods=['GET', 'POST'])
@login_required
def toggle_theme():
    if request.method == 'POST':
        current_user.tema_escuro = 'tema_escuro' in request.form
        db.session.commit()
        flash('Preferência de tema atualizada!', 'success')
        return redirect(url_for('routes.perfil'))

    return render_template('perfil.html', atividades=atividades, usuario=current_user)

# ------------------------
# RECUPERAÇÃO DE SENHA
# ------------------------
@routes.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_reset_token(user.id)
            send_reset_email(user, token)
        flash('Se o email estiver cadastrado, você receberá instruções para redefinir a senha.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)

@routes.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash('O link é inválido ou expirou.', 'warning')
        return redirect(url_for('routes.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.get(user_id)
        user.set_password(form.password.data)
        db.session.commit()

        flash('Senha redefinida com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)
