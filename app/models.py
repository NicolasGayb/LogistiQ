from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

# Modelo de usuário
class Usuario(db.Model, UserMixin):
    def set_password(self, password):
        self.senha = generate_password_hash(password)
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False) 
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # Data de cadastro do usuário
    tema_escuro = db.Column(db.Boolean, default=False)  # Preferência de tema
    notificacoes = db.Column(db.Boolean, default=True)  # Preferência de notificações
    ativo = db.Column(db.Boolean, default=True)  # Status da conta
    ultimo_login = db.Column(db.DateTime, nullable=True)  # Último login do usuário
    telefone = db.Column(db.String(20), nullable=True)  # Telefone do usuário
    endereco = db.Column(db.String(200), nullable=True)  # Endereço do usuário
    cargo = db.Column(db.String(100), nullable=True)  # Cargo do usuário na empresa
    data_inativacao = db.Column(db.DateTime, nullable=True)  # Data de inativação da conta
    observacoes = db.Column(db.Text, nullable=True)  # Observações adicionais
    avatar = db.Column(db.String(300), nullable=True)  # URL do avatar do usuário
    

    # Papel do usuário no sistema
    role = db.Column(db.String(20), nullable=False, default='usuario')  # valores: 'admin', 'usuario', 'supervisor', 'convidado'

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.username})>'

    # Métodos auxiliares para checar role
    def is_administrador(self):
        return self.role == 'administrador'

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
    data_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Modelo de Atividades
class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = db.relationship('Usuario', backref=db.backref('atividades', lazy=True))

