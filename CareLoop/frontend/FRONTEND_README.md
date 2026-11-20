# CareLoop Frontend

The CareLoop frontend uses plain HTML, CSS and JavaScript. FastAPI serves these pages from the same address as the API, so no separate frontend server is needed.

## Pages

| Page | Purpose |
|---|---|
| `index.html` | Dashboard with patient totals, prediction totals, risk split and recent predictions |
| `patients.html` | Search, filter, view, update, delete and predict for registered patients |
| `patient-form.html` | Register a patient or edit an existing patient |
| `result.html` | Show the latest prediction, patient summary and prediction history |
| `model.html` | Compare Decision Tree, Logistic Regression and Random Forest metrics |

## Run

From the main CareLoop folder:

```bash
python -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

FastAPI serves the frontend from `/app` and redirects `/` to the dashboard. The JavaScript calls the API on the same host.

## Database-first prediction flow

1. The patient form sends patient details to `POST /patients`.
2. FastAPI saves the details in the SQLite `careloop.db` database and returns a patient ID.
3. The frontend sends `POST /predict/{patient_id}`.
4. FastAPI retrieves the saved record from SQLite.
5. The backend applies the saved preprocessing object and the selected Logistic Regression model.
6. The backend stores the prediction in the `predictions` table.
7. The frontend displays the saved prediction result.

The frontend is an academic demonstration interface. Do not enter real patient-identifiable or confidential medical information.
