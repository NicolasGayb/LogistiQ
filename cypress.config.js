const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:5000", // endereço do Flask local
    viewportWidth: 1280,
    viewportHeight: 800,
    setupNodeEvents(on, config) {
      // eventos e plugins futuros
    },
  },
});
