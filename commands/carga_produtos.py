import random
from app import db
from app.models import Produto

# Lista de produtos base
nomes_base = [
    "Mouse", "Teclado", "Monitor", "Notebook", "Headset", "Webcam", "SSD",
    "HD Externo", "Pen Drive", "Placa de Vídeo", "Processador", "Memória RAM",
    "Roteador", "Fonte", "Gabinete", "Cooler", "Microfone", "Tablet",
    "Smartphone", "Carregador", "Cabo HDMI", "Mousepad", "Hub USB", "Caixa de Som",
    "Controle", "Drone", "Smartwatch", "Adaptador Bluetooth", "Leitor de Cartão"
]

# Sufixos para dar variedade
sufixos = ["Pro", "Plus", "Max", "Ultra", "Lite", "Edge", "Air", "Mini", "X", "S"]

# Quantos produtos gerar
quantidade_produtos = 40

for _ in range(quantidade_produtos):
    nome = f"{random.choice(nomes_base)} {random.choice(sufixos)}"
    quantidade = random.choice([5, 17, 26, 35, 57, 88, 300])
    preco = round(random.uniform(49.90, 8999.99), 2)

    produto = Produto(
        nome=nome,
        quantidade=quantidade,
        preco=preco
    )
    db.session.add(produto)

db.session.commit()
print(f"{quantidade_produtos} produtos gerados com sucesso!")
