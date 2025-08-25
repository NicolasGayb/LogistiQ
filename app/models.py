from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo de usuário
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    tema_escuro = db.Column(db.Boolean, default=False)  # Preferência de tema
    notificacoes = db.Column(db.Boolean, default=True)  # Preferência de notificações
    
    # Papel do usuário no sistema
    role = db.Column(db.String(20), nullable=False, default='usuario')  # valores: 'admin', 'usuario', 'supervisor', 'convidado'

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.username})>'

    # Métodos auxiliares para checar role
    def is_admin(self):
        return self.role == 'admin'

    def is_supervisor(self):
        return self.role == 'supervisor'

    def is_usuario(self):
        return self.role == 'usuario'

    def is_convidado(self):
        return self.role == 'convidado'

# Modelo de produtos do estoque
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Modelo de logs de movimentação
class HistoricoMovimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, nullable=True)
    produto_nome = db.Column(db.String(150), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    quantidade_anterior = db.Column(db.Integer, nullable=True)
    quantidade_nova = db.Column(db.Integer, nullable=True)
    motivo = db.Column(db.String(200), nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo de Atividades
class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref=db.backref('atividades', lazy=True))

