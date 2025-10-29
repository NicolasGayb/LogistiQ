describe('Smoke - LogistiQ', () => {
  it('carrega a página inicial corretamente', () => {
    cy.visit('/');
    cy.title().should('exist');
    cy.contains('LogistiQ');
  });
});
