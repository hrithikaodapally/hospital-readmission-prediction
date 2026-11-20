# CareLoop – Hospital Readmission Risk Prediction

CareLoop is an academic machine-learning project that estimates the possibility of 30-day hospital readmission for records based on the UCI Diabetes 130-US Hospitals dataset.

The project compares Decision Tree, Logistic Regression and Random Forest classifiers. Logistic Regression is selected for backend integration because it achieved the highest F1 score in the recorded model comparison. The other models are retained for comparison.

> **Academic demonstration only:** This model is not a medical diagnosis tool and must not be used to make real patient-care decisions. Do not enter real patient-identifiable or confidential medical information.

## Project structure

```text
CareLoop/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── patients.html
│   ├── patient-form.html
│   ├── result.html
│   ├── model.html
│   ├── css/
│   └── js/
│
├── data/
│   ├── diabetic_data.csv
│   ├── IDS_mapping.csv
│   └── processed/
│       ├── X_train_processed.pkl
│       ├── X_test_processed.pkl
│       ├── y_train.pkl
│       ├── y_test.pkl
│       ├── preprocessor.joblib
│       └── feature_info.joblib
│
├── preprocessing/
│   └── data_preprocessing.ipynb
│
├── models/
│   ├── decision_tree/
│   │   ├── decision_tree_training.ipynb
│   │   ├── model.joblib
│   │   └── metrics.json
│   ├── logistic_regression/
│   │   ├── logistic_regression_training.ipynb
│   │   ├── model.joblib
│   │   └── metrics.json
│   └── random_forest/
│       ├── random_forest_training.ipynb
│       ├── model.joblib
│       └── metrics.json
│
├── evaluation/
│   ├── MODEL_COMPARISON.md
│   ├── model_comparison.json
│   └── model_results.json
│
├── examples/
│   ├── patient_request.json
│   └── CareLoop_Postman_Collection.json
│
├── requirements.txt
└── start_server.bat
```

## 1. Install dependencies

Use Python 3.11 or newer and install the exact versions in requirements.txt. The saved model and preprocessor artifacts were serialized with scikit-learn 1.9.1.

From the CareLoop project folder, run:

```bash
python -m pip install -r requirements.txt
```

## 2. Model training notebooks

Model training is done using Jupyter Notebook (`.ipynb`), not training scripts.

Open the project folder in VS Code or Jupyter and run each notebook from top to bottom:

- `models/decision_tree/decision_tree_training.ipynb`
- `models/logistic_regression/logistic_regression_training.ipynb`
- `models/random_forest/random_forest_training.ipynb`

The notebooks use the existing files in `data/processed/`. They do not repeat the preprocessing step. Each notebook saves its trained model as `model.joblib` and evaluation results as `metrics.json`.

The current comparison is documented in `evaluation/MODEL_COMPARISON.md`.

## 3. Selected model

The comparison selected **Logistic Regression** based on the highest F1 score among the three baseline models.

| Model | Accuracy | Precision | Recall | F1 score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Decision Tree | 0.5974 | 0.1470 | 0.5769 | 0.2342 | 0.6075 |
| Logistic Regression | 0.6554 | 0.1665 | 0.5560 | **0.2562** | 0.6558 |
| Random Forest | 0.8524 | 0.2568 | 0.2022 | 0.2263 | 0.6730 |

These are baseline results on the recorded test split. They are modest, particularly in precision and recall. Accuracy alone is not a suitable way to judge performance on this imbalanced dataset.

## 4. Run CareLoop

Open a terminal in the main `CareLoop` folder and run:

```bash
python -m uvicorn backend.main:app --reload
```

Then open:

- Application: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

The SQLite database file `careloop.db` is created automatically when the backend starts.

## 5. Application workflow

1. Open the **New Patient** page.
2. Enter the patient information and choose **Save & predict risk**.
3. FastAPI validates the fields and saves the patient details into SQLite.
4. The backend returns a patient ID.
5. The frontend requests a prediction using that patient ID.
6. FastAPI retrieves the saved record from SQLite and applies `preprocessor.joblib`.
7. The selected Logistic Regression model (`models/logistic_regression/model.joblib`) makes the prediction.
8. FastAPI saves the prediction and probability in SQLite.
9. CareLoop displays the prediction result.

This is a database-first workflow: the model is not called directly with unsaved form data.

## 6. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API and loaded model |
| POST | `/patients` | Save a patient record |
| GET | `/patients` | List all patients and latest predictions |
| GET | `/patients/{id}` | Get one patient |
| PUT | `/patients/{id}` | Update a patient |
| DELETE | `/patients/{id}` | Delete a patient and prediction history |
| POST | `/predict/{id}` | Predict from a patient record already saved in SQLite |
| GET | `/predictions` | View prediction history |
| GET | `/stats` | Dashboard statistics |
| GET | `/model-info` | Model comparison metrics |

## 7. Test using Postman

First register a patient:

- Method: `POST`
- URL: `http://127.0.0.1:8000/patients`
- Body: `raw` → `JSON`
- Use the example in `examples/patient_request.json`.

Copy the `patient_id` from the response. Then run:

- Method: `POST`
- URL: `http://127.0.0.1:8000/predict/<patient_id>`

For example, if the API returned patient ID `1`, use:

`http://127.0.0.1:8000/predict/1`

The API response includes the prediction, result text, selected model and readmission probability.

## 8. Generate a public URL with ngrok

Keep FastAPI running in the first terminal. Open a second terminal and run:

```bash
ngrok http 8000
```

Copy the HTTPS forwarding address from ngrok. The public application is at that address, and the public API documentation is at:

`https://YOUR-NGROK-ADDRESS/docs`

The laptop, FastAPI process and ngrok tunnel must remain running while the public URL is being used. Never share your ngrok authentication token.

## 9. Database

CareLoop uses SQLite with two tables:

- `patients`: stores the submitted patient information as JSON, keyed by `patient_id`.
- `predictions`: stores each prediction and probability, linked to the patient ID.

The database is created automatically by the backend. The generated `careloop.db` file is local runtime data and should not be committed to GitHub.

## 10. Limitations

- This is a classroom prototype, not a validated clinical prediction system.
- Performance is limited by the recorded baseline metrics and class imbalance.
- The SQLite database is local to the machine running FastAPI.
- ngrok exposes the local application only while the server and tunnel are running.
- Avoid sending or storing real patient-identifiable or confidential health information.
