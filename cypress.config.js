const { defineConfig } = require('cypress');
const fs = require('fs');

module.exports = defineConfig({
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: {
    reportDir: 'cypress/reports',  // Diretório fixo e centralizado
    charts: true,
    overwrite: false,
    html: true,
    json: true,
    embeddedScreenshots: true,
    inlineAssets: true
  },

  e2e: {
    baseUrl: 'http://localhost:5000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

    setupNodeEvents(on, config) {
      // 🔹 Inicializa o reporter mochawesome
      require('cypress-mochawesome-reporter/plugin')(on);

      // 🔹 Task para deletar o banco de testes (executa via Node, funciona em qualquer SO)
      on('task', {
        deleteTestDB() {
          const path = 'instance/logistiq.db';
          try {
            if (fs.existsSync(path)) {
              fs.unlinkSync(path);
              console.log('🧹 Banco de teste apagado com sucesso!');
            } else {
              console.log('ℹ️ Nenhum banco de teste encontrado.');
            }
          } catch (err) {
            console.error('⚠️ Erro ao tentar apagar o banco:', err);
          }
          return null;
        },
      });

      // 🔹 Mensagem final após a execução completa
      on('after:run', () => {
        console.log('📊 Cypress executado — JSONs prontos para merge.');
      });

      return config;
    },
  },
});
