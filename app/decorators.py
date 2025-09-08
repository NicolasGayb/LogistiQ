from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import Usuario
from app import db
import logging

logger = logging.getLogger(__name__)

def role_required(*roles):
    """
    Decorador que permite acesso apenas a usuários autenticados
    cujos papéis estejam dentro da lista roles.
    
    - Se usado sem argumentos: restrição padrão para ("administrador", "supervisor")
    - Se usado com argumentos: aceita um ou mais papéis
    """

    # Caso usado sem parênteses: @role_required
    if roles and callable(roles[0]):
        f = roles[0]
        allowed_roles = ("administrador", "supervisor")

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Por favor, faça login para acessar esta página.", "warning")
                return redirect(url_for("login"))

            try:
                user = db.session.get(Usuario, current_user.id)
                if not user or user.role not in allowed_roles:
                    flash("Acesso negado: você não tem permissão para acessar esta página.", "danger")
                    return redirect(url_for("auth.login"))
            except SQLAlchemyError as e:
                logger.error(f"Erro ao verificar o papel do usuário: {e}")
                flash("Ocorreu um erro ao verificar suas permissões. Tente novamente mais tarde.", "danger")
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)
        return decorated_function

    # Caso usado com argumentos: @role_required("admin", "usuario")
    allowed_roles = roles or ("administrador", "supervisor")

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Por favor, faça login para acessar esta página.", "warning")
                return redirect(url_for("login"))

            try:
                user = db.session.get(Usuario, current_user.id)
                if not user or user.role not in allowed_roles:
                    flash("Acesso negado: você não tem permissão para acessar esta página.", "danger")
                    return redirect(url_for("auth.login"))
            except SQLAlchemyError as e:
                logger.error(f"Erro ao verificar o papel do usuário: {e}")
                flash("Ocorreu um erro ao verificar suas permissões. Tente novamente mais tarde.", "danger")
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)
        return decorated_function

    return decorator

# Uso:
# @app.route('/historico')
# @role_required("administrador", "supervisor")