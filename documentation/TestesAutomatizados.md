# 🧪 Guia de Testes Automatizados – LogistiQ

## 📘 Visão Geral

O LogistiQ utiliza **testes automatizados integrados** ao pipeline CI/CD para garantir a qualidade e a estabilidade contínua do sistema.

| Tipo de Teste | Framework | Objetivo |
|---------------|------------|-----------|
| **Unitários** | `pytest` | Validar regras de negócio e funções do backend Flask |
| **End-to-End (E2E)** | `Cypress` | Testar o fluxo completo da aplicação via interface web |

Esses testes são executados automaticamente no GitHub Actions a cada `push` ou `pull request` para a branch `main`.

---

## 🧠 Estrutura dos Testes

```
LogistiQ/
├── app/
│   ├── ... (código principal Flask)
│
├── tests/
│   ├── test_models.py          # Testes unitários de modelos e banco de dados
│   ├── test_routes.py          # Testes das rotas Flask
│   ├── test_auth.py            # Testes de autenticação e sessão
│   └── __init__.py
│
├── cypress/
│   ├── e2e/
│   │   ├── login.cy.js         # Testes do fluxo de login
│   │   ├── usuarios.cy.js      # Testes da aba de usuários (CRUD e filtros)
│   │   ├── produtos.cy.js      # Testes da aba de produtos
│   │   └── ...
│   ├── fixtures/               # Dados de exemplo (mock)
│   │   └── usuarios.json
│   ├── support/
│   │   ├── commands.js         # Comandos customizados (login, filtros, edição etc.)
│   │   └── e2e.js
│   ├── reports/                # Relatórios gerados automaticamente
│   └── cypress.config.js
│
└── .github/workflows/
    └── ci.yml                  # Pipeline automatizado (pytest + Cypress + deploy)
```

---

## ⚙️ Testes Unitários (Pytest)

Os testes unitários garantem que **cada componente do backend** funcione isoladamente.  
Eles usam o framework **Pytest** com integração ao **Flask-SQLAlchemy**.

### 🧩 Exemplo real de teste

```python
import pytest
from app import create_app, db
from app.models import Usuario

@pytest.fixture
def app():
    # Cria uma instância temporária da aplicação Flask para testes
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    # Cria um cliente de teste para enviar requisições HTTP simuladas
    return app.test_client()

def test_criar_usuario_no_banco(app):
    # Verifica se um novo usuário é criado corretamente no banco
    with app.app_context():
        usuario = Usuario(nome="Nicolas", email="teste@example.com", role="administrador")
        db.session.add(usuario)
        db.session.commit()

        resultado = Usuario.query.filter_by(email="teste@example.com").first()
        assert resultado is not None
        assert resultado.nome == "Nicolas"
        assert resultado.role == "administrador"
```

### ▶️ Como rodar localmente

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar todos os testes unitários
pytest -v

# Rodar com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

💡 **Dica:**  
Para visualizar a cobertura completa, gere o relatório em HTML:
```bash
pytest --cov=app --cov-report=html
```

---

## 🌐 Testes End-to-End (Cypress)

Os testes E2E simulam **a experiência do usuário final**, garantindo que o sistema funcione de ponta a ponta.

### 🧱 Estrutura principal

| Pasta | Função |
|--------|--------|
| `cypress/e2e/` | Contém os testes principais do sistema |
| `cypress/support/commands.js` | Armazena comandos customizados reutilizáveis |
| `cypress/reports/` | Armazena os relatórios automáticos do Mochawesome |

---

### 🧩 Exemplo de teste E2E

```javascript
describe('Gestão de Usuários - LogistiQ', () => {
  beforeEach(() => {
    cy.login('teste@example.com', 'senha_teste');
    cy.visit('/admin/usuarios');
  });

  it('deve exibir a tabela de usuários corretamente', () => {
    cy.get('table').should('exist');
    cy.contains('Nome').should('exist');
    cy.contains('Email').should('exist');
  });

  it('deve filtrar usuários do tipo Administrador', () => {
    cy.get('select[name="role"]').select('administrador');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', 'role=administrador');
    cy.get('tbody tr').should('contain', 'Administrador');
  });
});
```

---

### 🔧 Exemplo de comando customizado (reutilizável)

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, senha) => {
  cy.visit('/login');
  cy.get('input[name=email]').type(email);
  cy.get('input[name=senha]').type(senha);
  cy.get('button[type=submit]').click();
});
```

---

## 🧰 Rodando o Cypress localmente

### 1️⃣ Subir o servidor Flask
```bash
python run.py
```

### 2️⃣ Abrir o painel do Cypress
```bash
npx cypress open
```

### 3️⃣ Rodar em modo headless (sem interface)
```bash
npx cypress run --browser chrome
```

Os relatórios serão salvos automaticamente em:
```
cypress/reports/html/
```

---

## 🔄 Integração com o CI/CD

Toda vez que há um `push` na branch `main`, o pipeline executa:

| Etapa | Descrição |
|-------|------------|
| 🧠 `pytest` | Roda testes unitários e gera cobertura |
| 🌐 `cypress run` | Executa os testes E2E |
| 📊 `mochawesome` | Cria relatórios HTML e JSON |
| 🧾 `jq` | Atualiza histórico e documentação técnica |
| 🚀 `deploy` | Publica no GitHub Pages e no servidor DigitalOcean |

📍 **Resultados disponíveis em:**
- Dashboard QA: [https://nicolasgayb.github.io/LogistiQ](https://nicolasgayb.github.io/LogistiQ)  
- Documentação técnica: `docs/test-report.md`

---

## 🧩 Boas Práticas para Criar Testes

✅ Use **nomes descritivos** (`usuarios.cy.js`, `produtos.cy.js`)  
✅ Evite repetição — prefira comandos customizados (`commands.js`)  
✅ Use `data-testid` em elementos HTML para facilitar a seleção no Cypress  
✅ Utilize `beforeEach()` para preparar o ambiente  
✅ Sempre valide comportamento e não apenas interface  
✅ Mantenha commits organizados:
```
test: adiciona caso de teste para filtro de usuários
fix: corrige comportamento de filtro no Cypress
```

## 🏁 Conclusão

O sistema de testes do **LogistiQ** garante que:
- o **backend Flask** funcione de forma consistente,  
- o **frontend** entregue a experiência esperada,  
- e que cada entrega passe por **validação automática** de ponta a ponta.  

> 💬 “Testar é construir confiança. Automação é garantir que ela nunca se perca.”  
> — *Equipe LogistiQ*