from app import db
from app.models import Atividade
from datetime import datetime
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