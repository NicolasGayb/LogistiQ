const { defineConfig } = require('cypress');
const webpack = require('webpack');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    setupNodeEvents(on, config) {
      on('file:preprocessor', require('@cypress/webpack-preprocessor')({
        webpackOptions: {
          resolve: {
            fallback: {
              assert: require.resolve('assert/'),
              util: require.resolve('util/'),
            },
          },
        },
      }));
      return config;
    },
  },
});