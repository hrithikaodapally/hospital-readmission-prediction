// api.js – every call to the FastAPI backend goes through these functions (using fetch)

// If this page is served by FastAPI (http://host:8000/app/...) use the same address.
// If the HTML file is opened directly from disk, fall back to the local server.
const API_BASE = window.location.protocol.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";

// One helper that all other functions use
async function request(path, method = "GET", body = null) {
  const options = {
    method: method,
    // This header lets requests pass through the ngrok warning page
    headers: { "Content-Type": "application/json", "ngrok-skip-browser-warning": "true" },
  };
  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(API_BASE + path, options);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    // FastAPI sends the error text in "detail"
    let message = "Request failed (" + response.status + ")";
    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (data.detail && data.detail.message) {
      message = data.detail.message;
      if (data.detail.missing_fields) message += ": " + data.detail.missing_fields.join(", ");
    } else if (Array.isArray(data.detail)) {
      message = data.detail.map((d) => d.msg).join(", ");
    }
    throw new Error(message);
  }
  return data;
}

const api = {
  health: () => request("/health"),
  stats: () => request("/stats"),
  modelInfo: () => request("/model-info"),
  listPatients: () => request("/patients"),
  getPatient: (id) => request("/patients/" + id),
  addPatient: (patientData) => request("/patients", "POST", { patient_data: patientData }),
  updatePatient: (id, patientData) => request("/patients/" + id, "PUT", { patient_data: patientData }),
  deletePatient: (id) => request("/patients/" + id, "DELETE"),
  predict: (id) => request("/predict/" + id, "POST"),
  listPredictions: () => request("/predictions"),
};
