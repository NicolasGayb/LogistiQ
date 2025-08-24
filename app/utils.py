from app import db
from app.models import Atividade
from datetime import datetime
from functools import wraps
from flask import abort
from flask_login import current_user
import pytz

# Definir fuso horário UTC
utc = pytz.utc

def registrar_atividade(usuario, descricao):
    """
    Registra uma atividade no sistema vinculada a um usuário.
    """
    agora_utc = datetime.now(utc)

    atividade = Atividade(
        usuario_id=usuario.id,
        descricao=descricao,
        data=agora_utc
    )
    db.session.add(atividade)
    db.session.commit()

def listar_atividades(usuario):
    return Atividade.query.filter_by(usuario_id=usuario.id).order_by(Atividade.data.desc()).all()

def role_required(*roles):
    """Decorator para restringir acesso baseado em roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Usuário não logado
            if current_user.role not in roles:
                abort(403)  # Acesso negado
            return f(*args, **kwargs)
        return decorated_function
    return decorator    