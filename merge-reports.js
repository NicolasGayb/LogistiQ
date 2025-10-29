// merge-reports.js
const { merge } = require('mochawesome-merge');
const fs = require('fs');

(async () => {
  const jsonReport = await merge({ files: ['cypress/reports/*.json'] });
  fs.writeFileSync('cypress/reports/report.json', JSON.stringify(jsonReport, null, 2));
  console.log('✅ Relatórios mesclados com sucesso!');
})();
