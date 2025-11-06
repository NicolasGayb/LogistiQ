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
      // 🧹 Task universal para deletar o banco de testes
      // ======================================================
      on('task', {
        deleteTestDB() {
          const dbPath = path.join(__dirname, 'instance', 'logistiq.db');
          console.log(`🧩 Tentando apagar o banco de testes em: ${dbPath}`);

          try {
            if (fs.existsSync(dbPath)) {
              // Ajusta permissões antes de deletar (Windows pode travar o arquivo)
              try {
                fs.chmodSync(dbPath, 0o666);
              } catch {
                console.warn('⚠️ Aviso: não foi possível ajustar permissões antes de deletar.');
              }

              fs.unlinkSync(dbPath);
              console.log('✅ Banco de teste apagado com sucesso!');
              return { success: true, path: dbPath };
            } else {
              console.log('ℹ️ Nenhum banco de teste encontrado.');
              return { success: false, message: 'Arquivo não encontrado', path: dbPath };
            }
          } catch (err) {
            console.error('❌ Erro ao tentar apagar o banco:', err.message);
            return { success: false, error: err.message, path: dbPath };
          }
        },
      });

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
