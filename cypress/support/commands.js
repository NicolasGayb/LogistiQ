// Automação de comando personalizada para login 
Cypress.Commands.add('login', (email, password) => {
    cy.visit('/login');
    cy.get('input[name="email"]').type(email);
    cy.get('input[name="senha"]').type(password);
    cy.get('button[type="submit"]').click();
    });