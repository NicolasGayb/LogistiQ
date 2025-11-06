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

// Configuração do ambiente para testes com Admin
Cypress.Commands.add('setupAmbienteAdmin', () => {
  // 1. Resetar o banco de dados de testes
  cy.request('POST', '/api/test/reset_db').then((response) => {
    expect(response.status).to.eq(200);
    cy.log('🧹 Banco de testes resetado');
  });

  // 2. Cadastrar o admin
  cy.cadastroUsuario(
    'Admin Cypress',
    'admin@teste.com',
    'adminCypress',
    'Senha123!',
    'Senha123!'
  );

  // 3. Promover o usuário a admin via API
  cy.request('POST', '/api/test/promote_admin', {
    email: 'admin@teste.com'}).then((response) => {
        expect(response.status).to.eq(200);
        cy.log('🛡️ Usuário promovido a Admin');

  // 4. Fazer login com esse admin
  cy.login('admin@teste.com', 'Senha123!');
  cy.log('✅ Ambiente pronto com Admin logado');
});
});
// Comando para criar um produto
Cypress.Commands.add('criarProduto', (nome, quantidade, preco) => {
    cy.setupAmbienteAdmin();
            cy.visit('/produtos');
            cy.get('input[name="nome"]').type(nome);
            cy.get('input[name="quantidade"]').type(quantidade);
            cy.get('input[name="preco"]').type(preco);
            cy.get('button[type="submit"]').click();
    });