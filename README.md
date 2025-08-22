# 🧮 ControleEstoqueV2 · ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

Sistema web simples para controle de estoque, desenvolvido com Python e
Flask. Ideal para pequenos negócios ou como projeto de aprendizado.\
Agora com suporte a **PostgreSQL** para uso em produção e hospedagem em
plataformas como **Railway** ou **Render**.

## 📑 Tabela de Conteúdo

-   [Funcionalidades](#funcionalidades)
-   [Tecnologias Utilizadas](#tecnologias-utilizadas)
-   [Estrutura do Projeto](#estrutura-do-projeto)
-   [Instalação](#instalação)
-   [Uso](#uso)
-   [Banco de Dados](#banco-de-dados)
-   [Dependências](#dependências)
-   [Autor](#autor)

## ✅ Funcionalidades

-   👤 Cadastro e login de usuários com autenticação segura
-   📦 Registro, edição e exclusão de produtos
-   🗑 Correção da exclusão de produtos com tratamento de erros
-   📊 Visualização de estoque em tempo real
-   🔄 Controle de movimentações (entradas/saídas)
-   🌐 Suporte a **PostgreSQL** em produção e **SQLite** em ambiente
    local
-   🚀 Deploy simplificado no **Railway** ou **Render**

## 🛠 Tecnologias Utilizadas

-   [Python 3](https://www.python.org/)
-   [Flask](https://flask.palletsprojects.com/)
-   [Flask-Login](https://flask-login.readthedocs.io/)
-   [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
-   [SQLite](https://www.sqlite.org/index.html) (desenvolvimento local)
-   [PostgreSQL](https://www.postgresql.org/) (produção)

## 🚀 Estrutura do Projeto

    ControleEstoqueV2/
    │── app/
    │   ├── routes/
    │   │   ├── api_routes.py      # Rotas da API (JSON)
    │   │   ├── auth_routes.py     # Rotas de autenticação (login/registro)
    │   │   └── web_routes.py      # Rotas da aplicação web
    │   │
    │   ├── templates/             # Páginas HTML (login, registro, index, histórico)
    │   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
    │   ├── models.py              # Modelos do banco de dados
    │   └── __init__.py            # Inicialização do app Flask
    │
    │── run.py                     # Executa a aplicação localmente
    │── wsgi.py                    # Ponto de entrada para deploy (Render, Railway, AWS Beanstalk)
    │── requirements.txt           # Dependências do projeto
    │── Procfile                   # Configuração para deploy em produção
    │── README.md                  # Documentação do projeto

## Instalação

1.  Clone o repositório:

    ``` bash
    git clone https://github.com/NicolasGayb/ControleEstoqueV2.git
    ```

2.  Crie e ative um ambiente virtual (opcional):

    ``` bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate   # Windows
    ```

3.  Instale as dependências:

    ``` bash
    pip install -r requirements.txt
    ```

## Uso

1.  Execute o sistema localmente:

    ``` bash
    python run.py
    ```

2.  Acesse no navegador: `http://localhost:5000`

## Banco de Dados

-   Em **desenvolvimento**, o sistema usa **SQLite** automaticamente.
-   Em **produção**, basta configurar a variável de ambiente
    `DATABASE_URL` para o PostgreSQL (exemplo no Railway/Render).

Acessar o banco PostgreSQL pelo terminal:

``` bash
psql -h <host> -U <usuario> -d <banco>
```

## 🖥 Demonstração

![Tela inicial](app/static/demo.png)

## Dependências

Veja o arquivo `requirements.txt` para as bibliotecas necessárias.

## 👨‍💻 Autor

-   **Nicolas Gabriel Rodrigues Leal**
-   Email: <nicolasgbleal@gmail.com>
-   GitHub: [@NicolasGayb](https://github.com/NicolasGayb)
