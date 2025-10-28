describe('Gestão de Usuários - LogistiQ', () => {
    beforeEach(() => {
        // Realiza login antes de cada teste
        cy.login('teste@example.com', 'senha_teste');
        cy.visit('/admin/usuarios');
    });

    it('deve exibir a lista de usuários', () => {
        cy.get('table').should('exist');
        cy.contains('Nome').should('exist');
        cy.contains('Email').should('exist');
        cy.contains('Tipo').should('exist');
        cy.contains('Data Cadastro').should('exist');
    });

    it('deve filtrar usuários inativos', () => {
        cy.get('select[name="filtro_status"]').select('Inativos');
        cy.get('button[type="submit"]').click();
        cy.contains('Inativo').should('exist');
    });

    it('deve editar um usuário', () => {
        cy.contains('teste_usuario').parent('tr').within(() => {
            cy.get('a.edit-usuario').click();
        });
        cy.get('input[name="nome"]').clear().type('Usuário Editado');
        cy.get('button[type="submit"]').click();
        cy.contains('Usuário editado com sucesso').should('exist');
    });
});
    
        