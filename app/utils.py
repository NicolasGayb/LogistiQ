from app import mail, db
from app.models import Atividade, Usuario
from datetime import datetime, timedelta
from functools import wraps
from flask import abort, current_app, request, url_for
from flask_login import current_user
from flask_mail import Message
import jwt
import pytz

# Definir fuso horário UTC
utc = pytz.utc

# ------------------------
# ATIVIDADES
# ------------------------
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

# ------------------------
# DECORATOR DE ROLES
# ------------------------
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

# ------------------------
# TOKEN DE REDEFINIÇÃO DE SENHA
# ------------------------
def generate_reset_token(user_id, expires_sec=1800):
    """
    Gera um token JWT para redefinição de senha.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_sec)
    }
    token = jwt.encode(payload, str(current_app.config['JWT_SECRET_KEY']), algorithm='HS256')
    return token

def verify_reset_token(token):
    """
    Verifica a validade do token JWT.
    """
    try:
        payload = jwt.decode(token, str(current_app.config['JWT_SECRET_KEY']), algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ------------------------
# ENVIO DE EMAIL
# ------------------------
def send_reset_email(user: Usuario, token: str):
    """
    Envia um e-mail com link para redefinição de senha.
    """
    reset_url = url_for('routes.reset_password', token=token, _external=True)
    msg = Message(
        subject="Redefinição de senha",
        sender=current_app.config.get('MAIL_USERNAME', 'noreply@seusistema.com'),
        recipients=[user.email]
    )
    msg.body = f"""
    Olá {user.nome},

    Você solicitou redefinir sua senha. Clique no link abaixo para criar uma nova senha:

    {reset_url}

    Se você não solicitou, apenas ignore este e-mail.

    Atenciosamente,
    LogistiQ Team
    """
    mail.send(msg)
