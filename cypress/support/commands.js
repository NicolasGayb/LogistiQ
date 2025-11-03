// Automação de comando personalizada para login 
Cypress.Commands.add('login', (email, password) => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="senha"]').type(password);
    cy.get('button[type="submit"]').click();
});

// Automação de comando personalizada para cadastro de usuário
Cypress.Commands.add('cadastroUsuario', (nome, email, username, senha, confirmaSenha) => {
    cy.visit('/registro');
    cy.get('input[name="nome"]').type(nome);
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="username"]').type(username);
    cy.get('input[name="senha"]').type(senha);
    cy.get('input[name="confirmar"]').type(confirmaSenha);
    cy.get('button[type="submit"]').click();
});

// Comando para filtrar usuários por status
Cypress.Commands.add('filtrarUsuarioStatus', (status) => {
    cy.get('select[name="ativo"]').select(status);
    cy.get('button[type="submit"]').click();
});

// Comando para filtrar usuários por tipo
Cypress.Commands.add('filtrarUsuarioTipo', (tipo) => {
    cy.get('select[name="role"]').select(tipo);
    cy.get('button[type="submit"]').click();
});

// Comando para filtrar usuários por email
Cypress.Commands.add('filtrarUsuario', (email) => {
    cy.get('input[name="nome"]').type(email);
    cy.get('button[type="submit"]').click();
});

// Comando para editar um usuário específico
Cypress.Commands.add('editarUsuario', () => {
    cy.filtrarUsuario('teste@example.com');
    cy.contains('teste@example.com').parent('tr').within(() => {
            cy.get('a.btn.btn-warning.btn-sm').click();
        });
})

// Comando para submeter formulários
Cypress.Commands.add('submitForm', () => {
    cy.get('button[type="submit"]').click();
});