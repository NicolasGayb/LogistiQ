describe('Gestão de Produtos - LogistiQ', () => {
    beforeEach(() => {
        // Realiza login antes de cada teste
        cy.login('teste@example.com', 'Senha123!');
        cy.visit('/produtos');
    });

    // Verifica se a página de produtos foi carregada corretamente
    context('🧾 Estrutura da página', () => {
    it('deve exibir a tabela e cabeçalhos principais', () => {
        cy.get('table').should('exist');
        cy.get('th').contains('Nome');
        cy.get('th').contains('Quantidade');
        cy.get('th').contains('Preço');
        cy.get('th').contains('Valor Total');
    });
});
    // Testes de cadastro de produtos
    context('➕ Cadastro de Produtos', () => {
        it('deve cadastrar um novo produto com sucesso', () => {
            cy.get('input[name="nome"]').type('Produto Teste');
            cy.get('input[name="quantidade"]').type('10');
            cy.get('input[name="preco"]').type('100');
            cy.get('button[type="submit"]').click();
            cy.get('table').contains('td', 'Produto Teste').should('exist');
            });
         });
    });