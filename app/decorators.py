from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    """
    Decorator para rotas que exigem role específica.
    Exemplo de uso:
        @app.route('/admin')
        @role_required('administrador')
        def admin_dashboard():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                flash("Você não tem permissão para acessar esta página.", "danger")
                return redirect(url_for("routes.index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator
