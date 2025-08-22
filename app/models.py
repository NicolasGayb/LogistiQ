from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo de usuário com suporte ao Flask-Login
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

# Modelo de produtos do estoque
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Modelo de logs de atividades
class HistoricoMovimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, nullable=True)  # permite null
    produto_nome = db.Column(db.String(150), nullable=False)  # armazena o nome do produto
    usuario = db.Column(db.String(100), nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    quantidade_anterior = db.Column(db.Integer, nullable=True)
    quantidade_nova = db.Column(db.Integer, nullable=True)
    motivo = db.Column(db.String(200), nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

