# Aba Usuários - LogistiQ

A aba **Usuários** do sistema LogistiQ permite que administradores gerenciem todos os usuários cadastrados na plataforma. Nesta seção, é possível visualizar, criar, editar, excluir e filtrar usuários, com controle sobre seu status e permissões.

---

## 1. Acesso

- **Disponível apenas para:** Usuários com role `administrador`.
- **Rota:** `/admin/usuarios`
- **Requisitos:** Login autenticado.

---

## 2. Funcionalidades

### 2.1 Listagem de usuários

- Exibe uma tabela com os seguintes campos:
  - Nome
  - Username
  - Email
  - Tipo de usuário (role)
  - Status (ativo/inativo)
  - Data de cadastro (ajustada para fuso horário local)

- **Paginação:**
  - Cada página exibe até **25 usuários**.
  - Navegação entre páginas disponível.
  - O sistema usa paginação baseada em SQLAlchemy (`paginate`).

### 2.2 Filtros

É possível filtrar os usuários listados por:

| Campo           | Tipo       | Descrição                                      |
|-----------------|------------|------------------------------------------------|
| Nome            | Texto      | Pesquisa parcial no nome do usuário           |
| Email           | Texto      | Pesquisa parcial no email do usuário          |
| Status          | Dropdown   | Filtra por ativos (`sim`) ou inativos (`não`) |
| Tipo de usuário | Dropdown   | Filtra pelo role do usuário (`administrador`, `supervisor`, `usuario`, `convidado`) |

> Observação: Os filtros podem ser combinados, permitindo refinar a busca.

### 2.3 Ações sobre usuários

- **Criar Usuário**
  - Rota: `/admin/usuarios/criar`
  - Campos obrigatórios: `nome`, `username`, `email`, `role`, `senha`
  - O sistema impede duplicidade de username ou email.
  - Mensagens de erro ou sucesso exibidas via `flash`.

- **Editar Usuário**
  - Rota: `/admin/usuarios/editar/<id>`
  - Campos obrigatórios: `nome`, `username`, `email`, `role`
  - Senha pode ser deixada em branco para manter a atual.
  - Valida duplicidade de username ou email ignorando o próprio usuário.

- **Excluir Usuário**
  - Rota: `/admin/usuarios/excluir/<id>` (POST)
  - Remove permanentemente o usuário do sistema.
  - Mensagem de confirmação exibida via `flash`.

---

## 3. Mensagens de sistema

O sistema utiliza **mensagens flash** para informar:

- Sucesso na criação, edição ou exclusão de usuários.
- Erros de preenchimento obrigatório.
- Duplicidade de username ou email.

Exemplos:

- `"Usuário criado com sucesso!"`
- `"Preencha todos os campos obrigatórios!"`
- `"Já existe um usuário com esse username ou email!"`

---

## 4. Observações Técnicas

- A listagem utiliza **paginação do SQLAlchemy** para gerar links de navegação.
- Ajuste de data de cadastro é realizado para o fuso horário local.
- Apenas administradores conseguem acessar esta aba e realizar alterações.
- A tabela e filtros são renderizados dinamicamente via template Jinja2.

---

## 5. Layout (Resumo)

┌───────────────────────────────────────────────────────────┐
│ [Filtros: Nome | Email | Ativo | Tipo] [Botão Criar Usuário] │
├─────────┬──────────┬────────────┬───────────────┬─────────┤
│ Nome │ Username │ Email │ Tipo │ Status │
├─────────┼──────────┼────────────┼───────────────┼─────────┤
│ ... │ ... │ ... │ ... │ ... │
└─────────┴──────────┴────────────┴───────────────┴─────────┘
[Paginação: << 1 2 3 >>]

---

Documentação criada para uso interno da equipe e referência de desenvolvimento.
