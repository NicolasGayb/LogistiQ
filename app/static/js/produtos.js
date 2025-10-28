// =====================
// 📦 Gráficos de Produtos
// =====================
document.addEventListener("DOMContentLoaded", () => {
  // 🔹 Lê JSON embutido no template
  const raw = document.getElementById("estoque-data")?.textContent || "{}";
  const parsed = JSON.parse(raw);

  const estoqueLabels = parsed.labels || [];
  const estoqueQuantidades = parsed.quantidades || [];
  const estoqueValores = parsed.valores || [];

  // 🔸 Se não houver dados, não renderiza nada
  if (!estoqueLabels.length) return;

  const ctxQtd = document.getElementById("quantidadeChart").getContext("2d");
  const ctxVal = document.getElementById("valorChart").getContext("2d");

  // 🎨 Define as cores para modo claro e escuro
  function chartColors(dark) {
    return {
      bgQtd: dark ? "rgba(100,181,246,0.7)" : "rgba(33,150,243,0.6)",
      bgVal: dark ? "rgba(129,199,132,0.7)" : "rgba(76,175,80,0.6)",
      borderQtd: dark ? "#64b5f6" : "#2196f3",
      borderVal: dark ? "#81c784" : "#4caf50",
      font: dark ? "#f5f5f5" : "#222",
      grid: dark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)"
    };
  }

  let charts = [];

  // 🧱 Cria os gráficos com base no tema
  function buildCharts(dark) {
    const c = chartColors(dark);

    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: c.font } }
      },
      scales: {
        x: { ticks: { color: c.font }, grid: { color: c.grid } },
        y: { beginAtZero: true, ticks: { color: c.font }, grid: { color: c.grid } }
      }
    };

    // 📊 Gráfico de Quantidades
    const qtdChart = new Chart(ctxQtd, {
      type: "bar",
      data: {
        labels: estoqueLabels,
        datasets: [{
          label: "Quantidade",
          data: estoqueQuantidades,
          backgroundColor: c.bgQtd,
          borderColor: c.borderQtd,
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        ...commonOptions,
        plugins: {
          ...commonOptions.plugins,
          title: { display: true, text: "Quantidade de Produtos", color: c.font }
        }
      }
    });

    // 💰 Gráfico de Valores
    const valChart = new Chart(ctxVal, {
      type: "bar",
      data: {
        labels: estoqueLabels,
        datasets: [{
          label: "Valor Total (R$)",
          data: estoqueValores,
          backgroundColor: c.bgVal,
          borderColor: c.borderVal,
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        ...commonOptions,
        plugins: {
          ...commonOptions.plugins,
          title: { display: true, text: "Valor Total por Produto", color: c.font }
        }
      }
    });

    charts = [qtdChart, valChart];
  }

  // 🕶️ Inicializa de acordo com o tema atual
  const darkInitial = document.body.classList.contains("dark");
  buildCharts(darkInitial);

  // 🔄 Recria gráficos quando o tema mudar
  document.addEventListener("themechange", (ev) => {
    charts.forEach((c) => c.destroy());
    buildCharts(ev.detail.dark);
  });
});
