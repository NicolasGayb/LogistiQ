describe('Gestão de Usuários - LogistiQ', () => {
    beforeEach(() => {
        // Realiza login antes de cada teste
        cy.login('teste@example.com', 'Senha123!');
        cy.visit('/admin/usuarios');
    });

    // Verifica se a página de usuários foi carregada corretamente
    context('🧾 Estrutura da página', () => {
    it('deve exibir a tabela e cabeçalhos principais', () => {
        cy.get('table').should('exist');
        cy.get('th').contains('Nome');
        cy.get('th').contains('Email');
        cy.get('th').contains('Tipo');
        cy.get('th').contains('Data Cadastro');
    });
});

    context('🔍 Funcionalidades de filtro', () => {
    // Filtra usuários por nome e email  
    it('deve filtrar usuários por nome', () => {
        cy.filtrarUsuario('Teste Cypress');
        cy.url().should('include', 'nome=Teste+Cypress');
        cy.get('tbody tr').should('contain', 'Teste Cypress');
    });
    it('deve filtrar usuários por email', () => {
        cy.filtrarUsuario('teste@example.com');
        cy.url().should('include', 'nome=teste%40example.com');
        cy.get('tbody tr').should('contain', 'teste@example.com');
    });
    
    // Filtra usuários por tipo 
    it('deve filtrar usuários do tipo Administrador', () => {
        cy.filtrarUsuarioTipo('Administrador');
        cy.url().should('include', 'role=administrador');
        cy.get('tbody tr').should('contain', 'Administrador');
    });
    it('deve filtrar usuários do tipo Supervisor', () => {
        cy.filtrarUsuarioTipo('Supervisor');
        cy.url().should('include', 'role=supervisor');
        cy.get('tbody tr').should('contain', 'Supervisor');
    });
    it('deve filtrar usuários do tipo Usuário', () => {
        cy.filtrarUsuarioTipo('Usuário');
        cy.url().should('include', 'role=usuario');
        cy.get('tbody tr').should('contain', 'Usuario');
    });
    it('deve filtrar usuários do tipo Convidado', () => {
        cy.filtrarUsuarioTipo('Convidado');
        cy.url().should('include', 'role=convidado');
        cy.get('tbody tr').should('contain', 'Convidado');
    });

    // Filtra usuários por status
    it('deve filtrar usuários ativos', () => {
        cy.get('select[name="ativo"]').select('Ativo');
        cy.submitForm()
        cy.url().should('include', 'ativo=ativo');
        cy.get('tbody tr').should('contain', 'Ativo');
    });
    it('deve filtrar usuários inativos', () => {
        cy.get('select[name="ativo"]').select('Inativo');
        cy.submitForm()
        cy.url().should('include', 'ativo=inativo');
        cy.get('tbody tr').should('contain', 'Inativo');
    });
});

    context('✏️ Funcionalidade de edição', () => {
    // Edição de um usuário existente
    it('deve editar o nome de um usuário', () => {
        cy.editarUsuario();
        cy.get('input[name="nome"]').clear().type('Teste Cypress');
        cy.submitForm()
        cy.contains('Usuário atualizado com sucesso').should('be.visible');
    });
    it('deve editar o email de um usuário', () => {
        cy.editarUsuario();
        cy.get('input[name="email"]').clear().type('teste@example.com');
        cy.submitForm()
        cy.contains('Usuário atualizado com sucesso').should('be.visible');
    });
    it('deve editar o tipo de um usuário', () => {
        cy.editarUsuario();
        cy.get('select[name="role"]').select('Administrador');
        cy.submitForm()
        cy.contains('Usuário atualizado com sucesso').should('be.visible');
    });
    it('deve editar o status de um usuário', () => {
        cy.editarUsuario();
        cy.get('input[name="ativo"]').click();
        cy.submitForm()
        cy.contains('Usuário atualizado com sucesso').should('be.visible');
    });
    it('deve editar a senha de um usuário', () => {
        cy.editarUsuario();
        cy.get('input[name="senha"]').type('senha_teste');
        cy.submitForm()
        cy.contains('Usuário atualizado com sucesso').should('be.visible');
    });
});
});