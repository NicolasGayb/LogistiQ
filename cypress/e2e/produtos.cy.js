describe('Gestão de Produtos - LogistiQ', () => {

    // Verifica se a página de produtos foi carregada corretamente
    context('🧾 Estrutura da página', () => {
    it('deve exibir a tabela e cabeçalhos principais', () => {
        cy.setupAmbienteAdmin();
        cy.visit('/produtos');
        cy.get('table').should('exist');
        cy.get('th').contains('Nome');
        cy.get('th').contains('Quantidade');
        cy.get('th').contains('Preço');
        cy.get('th').contains('Valor Total');
    });
    it('deve exibir o gráfico de produtos', () => {
        cy.login('admin@teste.com', 'Senha123!');
        cy.visit('/produtos');
        cy.criarProduto('Produto Teste', 5, 50);
        cy.wait(1000); // Espera o gráfico carregar
        cy.get('#quantidadeChart').should('exist').and('be.visible');
        cy.get('#valorChart').should('exist').and('be.visible');
    });
});
    // Testes de cadastro de produtos
    context('➕ Cadastro de Produtos', () => {
        it('deve cadastrar um novo produto com sucesso', () => {
            cy.setupAmbienteAdmin();
            cy.visit('/produtos');
            cy.get('input[name="nome"]').type('Produto Teste');
            cy.get('input[name="quantidade"]').type('10');
            cy.get('input[name="preco"]').type('100');
            cy.get('button[type="submit"]').click();
            cy.get('table').contains('td', 'Produto Teste').should('exist');
            });

        it('deve editar um produto existente', () => {
            cy.login('admin@teste.com', 'Senha123!');
            cy.visit('/produtos');
            cy.get('table').contains('td', 'Produto Teste').parent('tr').within(() => {
                cy.get('input[name="quantidade"]').clear().type('20');
                cy.get('input[name="motivo"]').type('Ajuste de estoque');
                cy.get('button[type="submit"]').click();
            });
            cy.get('table').contains('td', '20').should('exist');
        });
    });
    // Testes de exclusão de produtos
    context('🗑️ Exclusão de Produtos', () => {
        it('deve excluir um produto existente', () => {
            cy.login('admin@teste.com', 'Senha123!');
            cy.visit('/produtos');
            cy.get('table').contains('td', 'Produto Teste');
            cy.get('.btn.btn-sm.btn-danger').click();
            cy.get('table').contains('td', 'Produto Teste').should('not.exist');
            cy.contains('removido com sucesso');
        });
    });
});