// patient-form.js – add a new patient or edit an existing one (?id=3)

const MAIN_MEDS = ["insulin", "metformin"];
const OTHER_MEDS = [
  "repaglinide", "nateglinide", "chlorpropamide", "glimepiride", "acetohexamide", "glipizide",
  "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol",
  "troglitazone", "tolazamide", "examide", "citoglipton", "glyburide-metformin",
  "glipizide-metformin", "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone",
];
const MED_CHOICES = [["No", "Not prescribed"], ["Steady", "Steady dose"], ["Up", "Dose increased"], ["Down", "Dose decreased"]];

// These fields must be sent as numbers, and these may be sent as null when empty
const NUMBER_FIELDS = ["time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications",
  "number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses"];
const NULLABLE_FIELDS = ["diag_2", "diag_3", "max_glu_serum", "A1Cresult"];

const SAMPLE = {
  patient_label: "Sample patient", race: "Caucasian", gender: "Female", age: "[60-70)",
  admission_type_id: "1", admission_source_id: "7", discharge_disposition_id: "1",
  medical_specialty: "InternalMedicine", time_in_hospital: 5, num_lab_procedures: 48,
  num_procedures: 1, num_medications: 16, number_outpatient: 0, number_emergency: 1,
  number_inpatient: 2, number_diagnoses: 8, diag_1: "428", diag_2: "250.8", diag_3: "401",
  max_glu_serum: "", A1Cresult: ">8", insulin: "Up", metformin: "No", change: "Ch", diabetesMed: "Yes",
};

const form = document.getElementById("patient-form");
const editId = new URLSearchParams(window.location.search).get("id");

function fillSelect(id, pairs) {
  const select = document.getElementById(id);
  select.innerHTML = pairs.map((p) => `<option value="${esc(p[0])}">${esc(p[1])}</option>`).join("");
}

function buildForm() {
  ["race", "age", "admission_type_id", "admission_source_id", "discharge_disposition_id", "medical_specialty"]
    .forEach((name) => fillSelect(name, OPTIONS[name]));
  // sensible defaults
  document.getElementById("discharge_disposition_id").value = "1";
  document.getElementById("admission_source_id").value = "7";
  document.getElementById("medical_specialty").value = "InternalMedicine";
  document.getElementById("age").value = "[60-70)";

  MAIN_MEDS.forEach((name) => fillSelect(name, MED_CHOICES));

  // The remaining drugs are created in a loop to keep the HTML short
  document.getElementById("other-meds").innerHTML = OTHER_MEDS.map((name) => `
    <div class="field"><label for="${name}">${name}</label>
      <select id="${name}" name="${name}" class="med">${MED_CHOICES.map((c) => `<option value="${c[0]}">${c[1]}</option>`).join("")}</select></div>`).join("");
}

function setValues(data) {
  Object.keys(data).forEach((key) => {
    const input = document.getElementById(key);
    if (input) input.value = data[key] ?? "";
  });
}

// Read the form and build the object the API expects
function readValues() {
  const data = {};
  new FormData(form).forEach((value, key) => { data[key] = value.trim(); });

  NUMBER_FIELDS.forEach((key) => { data[key] = Number(data[key]); });
  NULLABLE_FIELDS.forEach((key) => { if (data[key] === "") data[key] = null; });
  return data;
}

function validate(data) {
  if (!data.diag_1) return "Please enter the primary diagnosis code.";
  for (const key of NUMBER_FIELDS) {
    const input = document.getElementById(key);
    if (Number.isNaN(data[key]) || data[key] < Number(input.min) || data[key] > Number(input.max)) {
      return `${input.labels[0].textContent} must be between ${input.min} and ${input.max}.`;
    }
  }
  return null;
}

async function loadForEdit() {
  document.getElementById("form-title").textContent = "Edit patient #" + editId;
  document.getElementById("save-only").textContent = "Save changes";
  document.getElementById("save-predict").textContent = "Save & re-predict";
  try {
    const patient = await api.getPatient(editId);
    setValues(patient.patient_data);
  } catch (error) {
    showToast(error.message, "error");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const wantsPrediction = event.submitter.dataset.predict === "true";

  const data = readValues();
  const problem = validate(data);
  if (problem) { showToast(problem, "error"); return; }

  const buttons = form.querySelectorAll("button");
  buttons.forEach((b) => (b.disabled = true));

  try {
    let patientId;
    if (editId) {
      await api.updatePatient(editId, data);
      patientId = editId;
    } else {
      const saved = await api.addPatient(data);
      patientId = saved.patient_id;
    }

    if (wantsPrediction) {
      await api.predict(patientId);
      window.location.href = "result.html?id=" + patientId;
    } else {
      showToast("Patient saved", "success");
      setTimeout(() => (window.location.href = "patients.html"), 700);
    }
  } catch (error) {
    showToast(error.message, "error");
    buttons.forEach((b) => (b.disabled = false));
  }
});

document.getElementById("sample-btn").addEventListener("click", () => { setValues(SAMPLE); showToast("Sample data filled"); });

document.addEventListener("DOMContentLoaded", () => {
  buildForm();
  if (editId) loadForEdit();
});
