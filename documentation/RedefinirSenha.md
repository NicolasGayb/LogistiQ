# 🔑 Documentação Técnica – Redefinição de Senha

## 📌 Visão Geral

A funcionalidade de redefinição de senha permite que usuários que esqueceram sua senha possam criar uma nova senha de forma **segura**. Todo o processo é auditável, baseado em tokens **JWT temporários** e envio de email seguro via **TLS**.

---

## 🔄 Fluxo de Processo

```mermaid
flowchart TD
    A[👤 Usuário acessa "Esqueceu sua senha"] --> B[✉️ Preenche email]
    B --> C{📋 Email existe no banco?}
    C -- Não --> D[💬 Mensagem genérica de sucesso (sem expor conta)]
    C -- Sim --> E[🔐 Gera token JWT com user_id e expiração 30min]
    E --> F[📧 Envia email com link seguro de redefinição]
    F --> G[👆 Usuário clica no link]
    G --> H[🔑 Token JWT é verificado]
    H --> I{✅ Token válido e não expirado?}
    I -- Não --> J[⚠️ Erro: Token inválido ou expirado]
    I -- Sim --> K[📝 Usuário insere nova senha e confirma]
    K --> L[🔍 Valida senha e confirmação]
    L --> M{✅ Senha atende critérios de segurança?}
    M -- Não --> N[⚠️ Erro: Senha inválida]
    M -- Sim --> O[💾 Senha é hashada e salva no banco]
    O --> P[🗂️ Registro de atividade: Redefinição de senha]
    P --> Q[🎉 Usuário recebe confirmação de sucesso]
```

---

## 🛠️ Detalhes Técnicos

### 1️⃣ Solicitação de Redefinição

* Usuário acessa a página **"Esqueceu sua senha"** e informa o email.
* Backend valida se o email existe.
* Para **não expor contas existentes**, o sistema retorna a **mesma mensagem de sucesso** para emails válidos e inválidos.

### 2️⃣ Geração do Token JWT

* Token contém:

  * `user_id`: ID do usuário
  * `exp`: expiração em 30 minutos
* Algoritmo: **HS256**
* Chave secreta: `JWT_SECRET_KEY` em `.env`

```python
token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
```

### 3️⃣ Envio de Email Seguro

* Email enviado via **Flask-Mail** usando **TLS**.
* Remetente padrão: `MAIL_DEFAULT_SENDER` no `.env`
* Link enviado:

```
<FRONTEND_URL>/reset_password/<token>
```

### 4️⃣ Validação do Token

* Backend verifica:

  * Token válido
  * Token não expirado
* Tokens inválidos ou expirados retornam **mensagem de erro genérica**.

### 5️⃣ Redefinição de Senha

* Usuário informa a nova senha e confirmação.
* Validações:

  * Senha mínima de **8 caracteres**
  * Confirmação igual à senha
* Senha é **hashada** antes de salvar no banco:

```python
hashed_password = generate_password_hash(form.password.data)
user.password = hashed_password
db.session.commit()
```

### 6️⃣ Registro de Auditoria

* Toda redefinição é registrada no histórico:

  * Usuário
  * Ação: `Redefinir Senha`
  * Motivo: `Usuário redefiniu a senha`
  * Data e hora UTC

### 7️⃣ Feedback ao Usuário

* Após sucesso, usuário recebe **mensagem de confirmação**.
* Em caso de erro, mensagens genéricas são exibidas.

---

## 🔐 Segurança

* JWT com expiração curta (**30min**)
* Emails enviados via **TLS**
* Senhas **nunca armazenadas em texto plano**
* Histórico de atividades garante **rastreamento e auditoria**

---

## 📂 Arquivos Relacionados

* `app/routes/web_routes.py` → Rotas `forgot_password` e `reset_password`
* `app/utils.py` → Funções:

  * `generate_reset_token`
  * `verify_reset_token`
  * `send_reset_email`
* `app/templates/forgot_password.html` → Formulário de solicitação
* `app/templates/reset_password.html` → Formulário de redefinição

---

💡 **Dica de Segurança:**
Nunca exiba mensagens que confirmem se um email existe. Isso evita que atacantes descubram contas válidas.
