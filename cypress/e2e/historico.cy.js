describe('Histórico de Produtos - LogistiQ', () => {
    // Verifica se a página de histórico foi carregada corretamente
    context('🧾 Estrutura da página', () => {
        it('deve exibir a tabela e cabeçalhos principais', () => {
            cy.setupAmbienteAdmin();
            cy.criarProduto('Produto Teste', 10, 100);
            cy.visit('/historico');
            cy.get('table').should('exist');
            cy.get('th').contains('Data/Hora');
            cy.get('th').contains('Produto');
            cy.get('th').contains('Usuário');
            cy.get('th').contains('Ação');
            cy.get('th').contains('Qtd. Anterior');
            cy.get('th').contains('Qtd. Nova');
            cy.get('th').contains('Motivo');
        });
    });
    // Testes de visualização de histórico
    context('📜 Visualização de Histórico', () => {
        it('deve exibir o histórico de produtos', () => {
            cy.login('admin@teste.com', 'Senha123!');
            cy.visit('/historico');
            cy.get('table').should('exist');
            cy.get('table tbody tr').should('have.length.greaterThan', 0);
        });
    });
});