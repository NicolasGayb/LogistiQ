// Este script limpa o banco de testes antes de rodar as suítes de testes.
// Funciona apenas no Windows com PowerShell.

beforeEach(() => {
  cy.log('🧹 Limpando banco de dados de teste (Node)...')
  cy.task('deleteTestDB')
  cy.log('✅ Banco de dados de teste limpo com sucesso!')
})
