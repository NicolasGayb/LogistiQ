describe('Login - LogistiQ', () => {
  // Teste de cadastro de usuário
  it('deve cadastrar um novo usuário com sucesso', () => {
    cy.cadastroUsuario('Usuário Teste', 'teste@cypress.com', 'usuarioTesteCypress', 'Senha123!', 'Senha123!');
    cy.contains('Cadastro realizado com sucesso');
  });

  // Testes de login
  it('deve permitir login com as credenciais válidas', () => {
    cy.login('teste@example.com', 'senha_teste');
  })

  it('deve exibir mensagem de erro com credenciais inválidas', () => {
    cy.login('teste@invalido.com', 'senha_invalida');
  })

});