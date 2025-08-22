# app/routes/api_routes.py
from flask import Blueprint, jsonify, request
from ..models import Produto
from .. import db

api = Blueprint("api", __name__)

# Rota para listar todos os produtos
@api.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        "id": p.id,
        "nome": p.nome,
        "quantidade": p.quantidade,
        "preco": p.preco
    } for p in produtos])

# Rota para criar um novo produto
@api.route("/produtos", methods=["POST"])
def criar_produto():
    data = request.json
    novo_produto = Produto(
        nome=data["nome"],
        quantidade=data["quantidade"],
        preco=data["preco"]
    )
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({"message": "Produto criado com sucesso!"}), 201

# Rota para atualizar um produto existente
@api.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    data = request.json
    produto.nome = data.get("nome", produto.nome)
    produto.quantidade = data.get("quantidade", produto.quantidade)
    produto.preco = data.get("preco", produto.preco)
    db.session.commit()
    return jsonify({"message": "Produto atualizado com sucesso!"})

# Rota para deletar um produto
@api.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({"message": "Produto deletado com sucesso!"})

# Rota para obter detalhes de um produto específico
@api.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "preco": produto.preco
    })
