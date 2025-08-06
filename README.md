
# ControleEstoqueV2

Sistema web para controle de estoque, desenvolvido em Python com Flask. Permite cadastro, autenticação de usuários e gerenciamento de produtos.

## Funcionalidades
- Cadastro e login de usuários
- Registro, edição e exclusão de produtos
- Visualização do estoque
- Controle de movimentações

## Tecnologias Utilizadas
- Python 3
- Flask
- SQLite

## Estrutura do Projeto
```
ControleEstoqueV2/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   └── routes.py
│   └── templates/
│       ├── index.html
│       ├── login.html
│       └── registro.html
├── instance/
│   └── estoque.db
│   └── static/
│       └── style.css
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/NicolasGayb/ControleEstoqueV2.git
   ```
2. Crie e ative um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
1. Execute o sistema:
   ```bash
   python run.py
   ```
2. Acesse no navegador: `http://localhost:5000`

## Dependências
Veja o arquivo `requirements.txt` para as bibliotecas necessárias.

## Contato
Autor: Nicolas Gabriel Rodrigues Leal
Email: nicolasgbleal@gmail.com
