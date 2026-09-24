const form = document.querySelector("#assurance-form");
const content = document.querySelector("#content");
const source = document.querySelector("#source");
const submitButton = document.querySelector("#submit-button");
const emptyState = document.querySelector("#empty-state");
const resultContent = document.querySelector("#result-content");
const rawResult = document.querySelector("#raw-result");
let latestResult = null;

const example = `The contracting authority is preparing a public contract under the Procurement Act 2023. The procurement team must document the intended procedure, conditions of participation, award criteria, transparency notices and conflicts of interest. This material should be checked against the current official UK Government source and reviewed by an accountable procurement professional before it is used for a live tender decision.`;

function setText(selector, value) {
  document.querySelector(selector).textContent = value ?? "—";
}

function setLoading(active) {
  submitButton.disabled = active;
  submitButton.classList.toggle("loading", active);
}

function calibrationFrom(data) {
  return data.calibration_details || data.architecture_flow?.layer_1_skbuk || {};
}

function renderResult(data) {
  latestResult = data;
  const calibration = calibrationFrom(data);
  const flags = calibration.flags?.length ? calibration.flags : ["NO_CALIBRATION_FLAGS"];
  const status = data.status || "UNKNOWN";

  emptyState.hidden = true;
  resultContent.hidden = false;
  setText("#decision-status", status.replaceAll("_", " "));
  setText("#decision-badge", data.requires_human_review ? "REVIEW REQUIRED" : "INFORMATIONAL");
  setText("#correlation-id", data.correlation_id);
  setText("#result-source", data.source || source.value);
  setText("#calibration-score", calibration.calibration_score ?? "—");
  setText("#target-module", calibration.target_mouuk_routing ?? "—");
  document.querySelector("#decision-badge").classList.toggle("insufficient", status === "INSUFFICIENT_EVIDENCE");

  const list = document.querySelector("#flags-list");
  list.replaceChildren(...flags.map((flag) => {
    const item = document.createElement("li");
    item.textContent = flag;
    return item;
  }));
  rawResult.textContent = JSON.stringify(data, null, 2);
}

function renderError(message) {
  latestResult = null;
  emptyState.hidden = true;
  resultContent.hidden = false;
  resultContent.innerHTML = `<div class="error-message"><strong>Assessment unavailable</strong><br>${message}</div>`;
}

async function checkService() {
  const pill = document.querySelector("#service-pill");
  try {
    const response = await fetch("/api/v1/status", {headers: {Accept: "application/json"}});
    if (!response.ok) throw new Error("Service status unavailable");
    const data = await response.json();
    pill.className = "service-pill online";
    pill.innerHTML = "<span></span>Service online";
    setText("#gateway-state", "Online");
    setText("#module-count", data.canonical_mouuk_modules);
    setText("#service-version", data.version);
  } catch {
    pill.className = "service-pill offline";
    pill.innerHTML = "<span></span>Service unavailable";
    setText("#gateway-state", "Unavailable");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!content.value.trim()) return content.focus();
  setLoading(true);
  try {
    const response = await fetch("/api/v1/process-regulation", {
      method: "POST",
      headers: {"Content-Type": "application/json", Accept: "application/json"},
      body: JSON.stringify({content: content.value.trim(), source: source.value.trim() || "Unspecified"}),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail?.[0]?.msg || "The gateway rejected this request.");
    renderResult(data);
  } catch (error) {
    renderError(error.message || "Check the service and try again.");
  } finally {
    setLoading(false);
  }
});

content.addEventListener("input", () => setText("#char-count", `${content.value.length.toLocaleString()} characters`));
document.querySelector("#load-example").addEventListener("click", () => {
  content.value = example;
  content.dispatchEvent(new Event("input"));
  content.focus();
});
document.querySelector("#clear-form").addEventListener("click", () => {
  form.reset();
  content.dispatchEvent(new Event("input"));
  emptyState.hidden = false;
  resultContent.hidden = true;
  latestResult = null;
});
document.querySelector("#copy-result").addEventListener("click", async (event) => {
  if (!latestResult) return;
  await navigator.clipboard.writeText(JSON.stringify(latestResult, null, 2));
  const original = event.target.textContent;
  event.target.textContent = "Copied";
  setTimeout(() => { event.target.textContent = original; }, 1200);
});
document.querySelector("#download-result").addEventListener("click", () => {
  if (!latestResult) return;
  const blob = new Blob([JSON.stringify(latestResult, null, 2)], {type: "application/json"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `tods-decision-${latestResult.correlation_id || "record"}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});

checkService();
