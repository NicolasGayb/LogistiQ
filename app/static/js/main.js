// =====================
// 🌗 Alternar Tema (global)
// =====================
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("theme-toggle");
  const body = document.body;

  // 🧠 Recupera tema salvo
  const saved = localStorage.getItem("theme");
  const initialDark = saved ? saved === "dark" : body.classList.contains("dark");

  // 🪄 Função que aplica o tema
  function applyTheme(dark) {
    body.classList.toggle("dark", dark);
    body.classList.toggle("light", !dark); // opcional se tiver .light no CSS
    localStorage.setItem("theme", dark ? "dark" : "light");

    // 🔔 Notifica outras páginas/componentes (ex: gráficos)
    document.dispatchEvent(new CustomEvent("themechange", { detail: { dark } }));
  }

  // ⚙️ Define o estado inicial
  applyTheme(initialDark);
  if (toggle) toggle.checked = initialDark;

  // 🎚️ Listener do switch iOS
  if (toggle) {
    toggle.addEventListener("change", (e) => {
      applyTheme(e.target.checked);
    });
  }

  // 💡 Inicializa tooltips do Bootstrap
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));
});
