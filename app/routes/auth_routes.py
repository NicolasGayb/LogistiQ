# Rotas de autenticação de usuários (login, logout, registro)
from app.forms import RequestResetForm, ResetPasswordForm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario
from app.utils import registrar_atividade
import re

auth = Blueprint('auth', __name__)

# ------------------------
# Função auxiliar para validar senha
# ------------------------
def senha_valida(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos um número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return "A senha deve conter pelo menos um caractere especial."
    return None

# ------------------------
# LOGIN
# ------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            registrar_atividade(usuario, "Realizou login no sistema")
            flash('Login realizado com sucesso!')
            return redirect(url_for('routes.index'))
        else:
            flash('Email ou senha inválidos.')
    return render_template('login.html')

# ------------------------
# LOGOUT
# ------------------------
@auth.route('/logout')
@login_required
def logout():
    registrar_atividade(current_user, "Realizou logout do sistema")
    logout_user()
    flash('Você saiu da conta.')
    return redirect(url_for('auth.login'))

# ------------------------
# REGISTRO DE NOVO USUÁRIO
# ------------------------
@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        username = request.form['username']
        senha = request.form['senha']

        erro = senha_valida(senha)
        if erro:
            flash(erro)
            return redirect(url_for('auth.registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.')
            return redirect(url_for('auth.registro'))
        
        if Usuario.query.filter_by(username=username).first():
            flash('Usuário já existente.')
            return redirect(url_for('auth.registro'))

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            username=username,
            senha=generate_password_hash(senha)
        )
        db.session.add(novo_usuario)
        db.session.commit()

        # Registra atividade de cadastro
        registrar_atividade(novo_usuario, "Registrou uma nova conta no sistema")

        flash('Cadastro realizado com sucesso! Faça o login para acessar o sistema.')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

# ------------------------
# RECUPERAÇÃO DE SENHA
# ------------------------
@auth.route('/forgot_password', methods=['GET', 'POST'])
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

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash('O link é inválido ou expirou.', 'warning')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.get(user_id)
        user.set_password(form.password.data)
        db.session.commit()

        flash('Senha redefinida com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)
