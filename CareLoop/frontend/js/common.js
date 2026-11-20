// common.js – navigation bar, footer, toast messages and small helpers used by every page

const PAGES = [
  { file: "index.html", label: "Dashboard" },
  { file: "patients.html", label: "Patients" },
  { file: "patient-form.html", label: "New Patient" },
  { file: "model.html", label: "Model" },
];

function buildLayout() {
  const current = window.location.pathname.split("/").pop() || "index.html";

  const links = PAGES.map((p) => {
    const active = p.file === current || (current === "result.html" && p.file === "patients.html") ? "active" : "";
    return `<a href="${p.file}" class="${active}">${p.label}</a>`;
  }).join("");

  document.getElementById("topbar").innerHTML = `
    <div class="topbar-inner">
      <a class="logo" href="index.html"><span class="logo-mark">✚</span> CareLoop</a>
      <span class="api-status"><span id="status-dot" class="status-dot"></span><span id="status-text">Checking API…</span></span>
      <nav class="nav">${links}</nav>
    </div>`;

  document.body.insertAdjacentHTML("beforeend",
    `<footer>Academic demonstration model – not for real patient-care decisions.</footer><div id="toast-area"></div>`);

  checkApi();
}

// Show whether the backend is reachable
async function checkApi() {
  const dot = document.getElementById("status-dot");
  const text = document.getElementById("status-text");
  try {
    const health = await api.health();
    dot.className = "status-dot up";
    text.textContent = "API online · " + health.model;
  } catch (error) {
    dot.className = "status-dot down";
    text.textContent = "API offline";
  }
}

function showToast(message, type = "") {
  const toast = document.createElement("div");
  toast.className = "toast " + type;
  toast.textContent = message;
  document.getElementById("toast-area").appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// Escape text before putting it inside innerHTML
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// The model flags a patient (prediction = 1) when probability is 0.5 or more.
// Between 0.25 and 0.5 we show "Elevated" as an early warning, below that "Low".
function riskLevel(probability, prediction) {
  if (prediction === 1 || probability >= 0.5) return { name: "High", css: "high" };
  if (probability >= 0.25) return { name: "Elevated", css: "mid" };
  return { name: "Low", css: "low" };
}

function percent(value) {
  return (value * 100).toFixed(1) + "%";
}

function optionLabel(group, value) {
  const found = (OPTIONS[group] || []).find((o) => o[0] === String(value));
  return found ? found[1] : value;
}

// Load Google Charts safely: if the Google script could not be loaded (offline), the page still works
function loadCharts(packages, drawFunction, containerIds) {
  if (!window.google || !google.charts) {
    containerIds.forEach((id) => {
      const box = document.getElementById(id);
      if (box) box.innerHTML = `<div class="empty">Charts need an internet connection (Google Charts).</div>`;
    });
    return;
  }
  google.charts.load("current", { packages: packages });
  google.charts.setOnLoadCallback(drawFunction);
}

document.addEventListener("DOMContentLoaded", buildLayout);
