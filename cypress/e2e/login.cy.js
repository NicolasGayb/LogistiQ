describe('Login - LogistiQ', () => {
  it('deve permitir login com as credenciais válidas', () => {
    cy.login('teste@example.com', 'senha_teste');
  })

  it('deve exibir mensagem de erro com credenciais inválidas', () => {
    cy.login('teste@invalido.com', 'senha_invalida');
  })
});