# 🧮 LogistiQ · ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue) ![License](https://img.shields.io/badge/License-MIT-green)

Sistema web simples para **gestão e controle de processos**, desenvolvido com Python e Flask. Ideal para aprendizado e projetos de portfólio.
Agora com suporte a **PostgreSQL** para produção, hospedagem própria no **DigitalOcean** e domínio oficial: [logistiq.studio](https://logistiq.studio).

---

## 📑 Tabela de Conteúdo

* [Funcionalidades](#funcionalidades)
* [Destaques Visuais](#destaques-visuais)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Instalação](#instalação)
* [Uso](#uso)
* [Banco de Dados](#banco-de-dados)
* [Contributing](#contributing)
* [Code of Conduct](#code-of-conduct)
* [Dependências](#dependências)
* [Autor](#autor)

---

## ✅ Funcionalidades

* 👤 Cadastro e login de usuários com autenticação segura
* 📦 Registro, edição e exclusão de registros/processos
* 📊 Visualização de dados em tempo real
* 🔄 Controle de movimentações e alterações
* 🌐 Suporte a **PostgreSQL** em produção e **SQLite** em ambiente local
* 🌙 Modo escuro completo para interface
* 📈 Gráficos interativos de métricas importantes
* 📝 Perfil do usuário com histórico de atividades e configurações personalizadas

---

## ✨ Destaques Visuais

* **Tema Escuro/Claro:** alternância de tema em cards, tabelas e formulários
* **Gráficos Dinâmicos:** gráficos interativos atualizados em tempo real
* **Inputs e Formulários Estilizados:** campos adaptam cores ao tema ativo
* **Perfil do Usuário:** avatar, histórico, notificações e configurações de tema
* **Feedback Visual:** mensagens, badges, alertas e tooltips aprimorados
* **Hover Effects:** efeitos sutis para maior interatividade

---

## 🛠 Tecnologias Utilizadas

* ![Python](https://img.shields.io/badge/Python-3.10-blue) [Python 3](https://www.python.org/)
* ![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey) [Flask](https://flask.palletsprojects.com/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
* [SQLite](https://www.sqlite.org/index.html) (desenvolvimento local)
* ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue) [PostgreSQL](https://www.postgresql.org/) (produção)
* [Bootstrap 5](https://getbootstrap.com/)
* [Chart.js](https://www.chartjs.org/)
* ![License](https://img.shields.io/badge/License-MIT-green) MIT License

---

## 🚀 Estrutura do Projeto

```
LogistiQ/
│── app/
│   ├── routes/
│   │   ├── api_routes.py
│   │   ├── auth_routes.py
│   │   └── web_routes.py
│   ├── templates/
│   ├── static/
│   ├── models.py
│   └── __init__.py
│── run.py
│── requirements.txt
│── README.md
│── CONTRIBUTING.md
│── CODE_OF_CONDUCT.md
```

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/NicolasGayb/LogistiQ.git
```

2. Crie e ative um ambiente virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Uso

1. Execute o sistema localmente:

```bash
python run.py
```

2. Acesse no navegador: `http://localhost:5000`
3. Em produção, acesse: [logistiq.studio](https://logistiq.studio)

---

## Banco de Dados

* **Desenvolvimento:** SQLite automaticamente
* **Produção:** Configure a variável de ambiente `DATABASE_URL` para PostgreSQL

Exemplo de acesso ao PostgreSQL pelo terminal:

```bash
psql -h <host> -U <usuario> -d <banco>
```

---

## Contributing

Obrigado por se interessar em contribuir para o LogistiQ! 🙌

### Como contribuir

1. **Reportar bugs**

   * Use nosso template de **Bug Report**.
   * Forneça informações claras e reproduzíveis.

2. **Sugerir melhorias ou novas funcionalidades**

   * Use nosso template de **Feature Request**.
   * Explique o problema e como a sugestão ajuda o projeto.

3. **Pull Requests**

   * Crie uma branch nova para cada feature ou correção:

```bash
git checkout -b feature/nova-feature
```

* Faça commits claros e descritivos:

```bash
git commit -m "Descrição clara do que foi feito"
```

* Abra um PR explicando as mudanças.

4. **Discussões e dúvidas**

   * Use o [Discussions do GitHub](https://github.com/NicolasGayb/LogistiQ/discussions) para perguntas e ideias.

### Boas práticas

* Siga o [Código de Conduta](CODE_OF_CONDUCT.md)
* Seja respeitoso e colaborativo
* Mantenha o repositório organizado

---

## Code of Conduct

O LogistiQ adota o seguinte **Código de Conduta**:

* Seja **respeitoso e inclusivo** em todas as interações
* Evite linguagem ofensiva, assédio ou discriminação
* Reporte condutas inadequadas aos mantenedores
* Contribua para um ambiente **positivo e colaborativo**

Para mais detalhes, veja o arquivo [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## 🖥 Demonstração

![Tela inicial](app/static/demo.png)

---

## Dependências

Veja o arquivo `requirements.txt` para as bibliotecas necessárias.

---

## 👨‍💻 Autor

* **Nicolas Gabriel Rodrigues Leal**
* Email: [nicolasgbleal@gmail.com](mailto:nicolasgbleal@gmail.com)
* GitHub: [@NicolasGayb](https://github.com/NicolasGayb)

