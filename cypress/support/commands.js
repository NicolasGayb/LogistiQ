// Automação de comando personalizada para login 
Cypress.Commands.add('login', (email, password) => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="senha"]').type(password);
    cy.get('button[type="submit"]').click();
    });

Cypress.Commands.add('filtrarUsuarioStatus', (status) => {
    cy.get('select[name="ativo"]').select(status);
    cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('filtrarUsuarioTipo', (tipo) => {
    cy.get('select[name="role"]').select(tipo);
    cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('filtrarUsuario', (email) => {
    cy.get('input[name="nome"]').type(email);
    cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('editarUsuario', () => {
    cy.filtrarUsuario('teste@example.com');
    cy.contains('teste@example.com').parent('tr').within(() => {
            cy.get('a.btn.btn-warning.btn-sm').click();
        });
})

Cypress.Commands.add('submitForm', () => {
    cy.get('button[type="submit"]').click();
});