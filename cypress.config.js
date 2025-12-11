const { defineConfig } = require('cypress');
const fs = require('fs');
const path = require('path');

module.exports = defineConfig({
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: {
    reportDir: 'cypress/reports',  // Diretório fixo e centralizado
    charts: true,
    overwrite: false,
    html: true,
    json: true,
    embeddedScreenshots: true,
    inlineAssets: true,
  },

  e2e: {
    baseUrl: 'http://localhost:5000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

    setupNodeEvents(on, config) {
      // 🔹 Inicializa o reporter mochawesome
      require('cypress-mochawesome-reporter/plugin')(on);

      // ======================================================
      // 📊 Log após execução completa dos testes
      // ======================================================
      on('after:run', () => {
        console.log('📊 Cypress executado — relatórios JSON prontos para merge.');
      });

      return config;
    },
  },
});
