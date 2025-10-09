from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Usuario, db
from app.decorators import role_required
from werkzeug.security import generate_password_hash
from datetime import timedelta, datetime
from sqlalchemy import or_
from math import ceil

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# -----------------------------
# Listar usuários com filtro
# -----------------------------
@admin_bp.route("/usuarios")
@login_required
@role_required("administrador")
def usuarios():
    page = request.args.get("page", 1, type=int)
    filtro_nome = request.args.get("nome", "", type=str)
    filtro_email = request.args.get("email", "", type=str)
    filtro_ativo = request.args.get("ativo", "", type=str)
    filtro_role = request.args.get("role", "todos", type=str)

    query = Usuario.query

    if filtro_nome:
        query = query.filter(Usuario.nome.ilike(f"%{filtro_nome}%"))
    if filtro_email:
        query = query.filter(Usuario.email.ilike(f"%{filtro_email}%"))
    if filtro_ativo == "sim":
        query = query.filter(Usuario.ativo.is_(True))
    elif filtro_ativo == "nao":
        query = query.filter(Usuario.ativo.is_(False))
    if filtro_role != "todos":
        query = query.filter(Usuario.role == filtro_role)

    # Usando paginate do SQLAlchemy para criar objeto Pagination
    usuarios_pag = query.order_by(Usuario.id).paginate(page=page, per_page=25, error_out=False)

    # Ajustar horário apenas na lista de itens da página
    for u in usuarios_pag.items:
        if u.data_cadastro:
            u.data_cadastro_ajustada = u.data_cadastro - timedelta(hours=3)
        else:
            u.data_cadastro_ajustada = None

    return render_template(
        "admin/usuarios.html",
        usuarios=usuarios_pag,
        filtro_nome=filtro_nome,
        filtro_email=filtro_email,
        filtro_ativo=filtro_ativo,
        filtro_role=filtro_role
    )
# -----------------------------
# Criar usuário
# -----------------------------
@admin_bp.route("/usuarios/criar", methods=["GET", "POST"])
@login_required
@role_required("administrador")
def criar_usuario():
    if request.method == "POST":
        nome = request.form.get("nome")
        username = request.form.get("username")
        email = request.form.get("email")
        senha = request.form.get("senha")
        role = request.form.get("role")
        ativo = bool(request.form.get("ativo"))

        # Validar campos obrigatórios
        if not nome or not username or not email or not role or not senha:
            flash("Preencha todos os campos obrigatórios, incluindo a senha!", "danger")
            return redirect(url_for("admin.criar_usuario"))

        # Verificar duplicidade
        if Usuario.query.filter((Usuario.username == username) | (Usuario.email == email)).first():
            flash("Já existe um usuário com esse username ou email!", "danger")
            return redirect(url_for("admin.criar_usuario"))

        # Criar usuário
        novo_usuario = Usuario(
            nome=nome,
            username=username,
            email=email,
            senha=generate_password_hash(senha, method="scrypt"),
            data_cadastro=datetime.utcnow(),
            role=role,
            ativo=ativo,
        )

        db.session.add(novo_usuario)
        db.session.commit()
        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("admin.usuarios"))

    return render_template("admin/criar_usuario.html")
# -----------------------------
# Editar usuário
# -----------------------------
@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("administrador")
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":
        nome = request.form.get("nome")
        username = request.form.get("username")
        email = request.form.get("email")
        senha = request.form.get("senha")
        role = request.form.get("role")
        ativo = bool(request.form.get("ativo"))

        # Validar campos obrigatórios
        if not nome or not username or not email or not role:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("admin.editar_usuario", id=id))

        # Verificar duplicidade (ignorando o próprio usuário)
        if Usuario.query.filter((Usuario.username == username) & (Usuario.id != id)).first():
            flash("Já existe outro usuário com esse username!", "danger")
            return redirect(url_for("admin.editar_usuario", id=id))

        if Usuario.query.filter((Usuario.email == email) & (Usuario.id != id)).first():
            flash("Já existe outro usuário com esse email!", "danger")
            return redirect(url_for("admin.editar_usuario", id=id))

        # Atualizar dados
        usuario.nome = nome
        usuario.username = username
        usuario.email = email
        usuario.role = role
        usuario.ativo = ativo

        # Atualizar senha apenas se preenchida
        if senha:
            usuario.senha = generate_password_hash(senha, method="scrypt")

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("admin.usuarios"))

    return render_template("admin/editar_usuario.html", usuario=usuario)

# -----------------------------
# Excluir usuário
# -----------------------------
@admin_bp.route("/usuarios/excluir/<int:id>", methods=["POST"])
@login_required
@role_required("administrador")
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for("admin.usuarios"))