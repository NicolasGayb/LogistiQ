from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
import random

app = create_app()

def gerar_nome():
    nomes = ["Ana", "Bruno", "Carla", "Daniel", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana"]
    sobrenomes = ["Silva", "Souza", "Costa", "Oliveira", "Pereira", "Lima", "Gomes", "Ribeiro", "Almeida", "Nascimento"]
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def gerar_username(nome):
    return nome.split()[0].lower() + str(random.randint(100, 999))

def gerar_email(username):
    dominios = ["example.com", "mail.com", "test.com"]
    return f"{username}@{random.choice(dominios)}"

def gerar_role():
    return random.choice(['administrador', 'usuario', 'supervisor', 'convidado'])

TOTAL_USUARIOS = 200
LOTE_SIZE = 20

with app.app_context():
    for i in range(0, TOTAL_USUARIOS, LOTE_SIZE):
        lote = []
        for j in range(LOTE_SIZE):
            nome = gerar_nome()
            username = gerar_username(nome)
            email = gerar_email(username)
            senha = generate_password_hash("senha123")
            role = gerar_role()
            usuario = Usuario(
                nome=nome,
                username=username,
                email=email,
                senha=senha,
                role=role,
                data_cadastro=datetime.now(timezone.utc),
                ativo=True
            )
            lote.append(usuario)
        db.session.bulk_save_objects(lote)
        db.session.commit()
        print(f"Lote de {LOTE_SIZE} usuários inserido. Total até agora: {i + LOTE_SIZE}")

    print(f"{TOTAL_USUARIOS} usuários criados com sucesso!")