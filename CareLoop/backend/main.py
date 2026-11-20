"""
CareLoop - Hospital Readmission Prediction
FastAPI backend that serves the selected Logistic Regression model.

Patient information is saved to SQLite before a prediction is created.
The prediction endpoint accepts a patient ID, reads that patient's saved
record, applies the saved preprocessing steps, runs the model, and stores
the result in SQLite.
"""

from contextlib import closing
from pathlib import Path
import json
import sqlite3
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# -------------------- Project files --------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_FOLDER / "models" / "logistic_regression" / "model.joblib"
PREPROCESSOR_PATH = PROJECT_FOLDER / "data" / "processed" / "preprocessor.joblib"
FEATURE_INFO_PATH = PROJECT_FOLDER / "data" / "processed" / "feature_info.joblib"
DATABASE_PATH = PROJECT_FOLDER / "careloop.db"
FRONTEND_FOLDER = PROJECT_FOLDER / "frontend"
MODEL_COMPARISON_PATH = PROJECT_FOLDER / "evaluation" / "model_comparison.json"

MODEL_NAME = "Logistic Regression"


# Load the trained model and preprocessing object once when the API starts.
try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    feature_info = joblib.load(FEATURE_INFO_PATH)
    feature_names = feature_info["feature_names"]
except FileNotFoundError as error:
    raise RuntimeError(
        "A required model file was not found. Check the models/logistic_regression "
        "and data/processed folders."
    ) from error
except Exception as error:
    raise RuntimeError(
        "Could not load the saved model or preprocessor. Use the same "
        "scikit-learn version that was used to train the model."
    ) from error


app = FastAPI(
    title="CareLoop API",
    description="Hospital readmission risk prediction for an academic project.",
    version="1.0.0",
)


# -------------------- Request format --------------------

class PatientInput(BaseModel):
    patient_data: dict[str, Any] = Field(
        ..., description="Patient information entered in the CareLoop form."
    )


# -------------------- Database functions --------------------

def get_connection():
    """Open a connection to the CareLoop SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    """Create the patient and prediction tables when the server starts."""
    with closing(get_connection()) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_data TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                prediction INTEGER NOT NULL,
                probability REAL NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        """)
        connection.commit()


def check_required_fields(patient_data: dict[str, Any]):
    """Check that the patient record contains all model input fields."""
    missing_fields = [name for name in feature_names if name not in patient_data]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Some patient fields are missing.",
                "missing_fields": missing_fields,
            },
        )


def make_model_input(patient_data: dict[str, Any]) -> pd.DataFrame:
    """Arrange saved patient details in the same order used during training."""
    patient_frame = pd.DataFrame(
        [{name: patient_data.get(name) for name in feature_names}],
        columns=feature_names,
    )

    # These identifier columns were treated as categorical values during preprocessing.
    for column in [
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id",
    ]:
        if column in patient_frame.columns:
            patient_frame[column] = patient_frame[column].astype("str")

    return patient_frame


# Create the tables as soon as the application starts.
create_tables()


# -------------------- Basic routes --------------------

@app.get("/")
def home():
    """Open the CareLoop frontend from the project root URL."""
    if FRONTEND_FOLDER.is_dir():
        return RedirectResponse(url="/app/index.html")
    return {"message": "CareLoop API is running. Open /docs to test the API."}


@app.get("/health")
def health():
    """Check whether the API and selected model are available."""
    return {
        "status": "ok",
        "project": "CareLoop",
        "model": MODEL_NAME,
    }


# -------------------- Patient routes --------------------

@app.post("/patients")
def add_patient(patient: PatientInput):
    """
    Save a patient record first.
    The frontend can then request a prediction using the returned patient ID.
    """
    check_required_fields(patient.patient_data)

    patient_json = json.dumps(patient.patient_data)

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "INSERT INTO patients (patient_data) VALUES (?)",
            (patient_json,),
        )
        patient_id = cursor.lastrowid
        connection.commit()

    return {
        "message": "Patient details saved successfully.",
        "patient_id": patient_id,
    }


@app.get("/patients")
def list_patients():
    """Return all patients with the latest prediction, if available."""
    with closing(get_connection()) as connection:
        rows = connection.execute("""
            SELECT
                p.patient_id,
                p.patient_data,
                pr.prediction_id,
                pr.prediction,
                pr.probability
            FROM patients AS p
            LEFT JOIN predictions AS pr
                ON pr.prediction_id = (
                    SELECT MAX(prediction_id)
                    FROM predictions
                    WHERE patient_id = p.patient_id
                )
            ORDER BY p.patient_id DESC
        """).fetchall()

    patients = []
    for row in rows:
        latest_prediction = None
        if row[2] is not None:
            latest_prediction = {
                "prediction_id": row[2],
                "prediction": row[3],
                "readmission_probability": round(float(row[4]), 4),
            }

        patients.append({
            "patient_id": row[0],
            "patient_data": json.loads(row[1]),
            "latest_prediction": latest_prediction,
        })

    return patients


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    """Return one saved patient record."""
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT patient_id, patient_data FROM patients WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Patient not found.")

    return {
        "patient_id": row[0],
        "patient_data": json.loads(row[1]),
    }


@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientInput):
    """Update the patient record. Existing prediction history is kept."""
    check_required_fields(patient.patient_data)

    with closing(get_connection()) as connection:
        cursor = connection.execute(
            "UPDATE patients SET patient_data = ? WHERE patient_id = ?",
            (json.dumps(patient.patient_data), patient_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found.")
        connection.commit()

    return {
        "message": "Patient details updated successfully.",
        "patient_id": patient_id,
    }


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    """Delete a patient and the predictions saved for that patient."""
    with closing(get_connection()) as connection:
        exists = connection.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()

        if exists is None:
            raise HTTPException(status_code=404, detail="Patient not found.")

        connection.execute(
            "DELETE FROM predictions WHERE patient_id = ?",
            (patient_id,),
        )
        connection.execute(
            "DELETE FROM patients WHERE patient_id = ?",
            (patient_id,),
        )
        connection.commit()

    return {
        "message": "Patient and prediction history deleted successfully.",
        "patient_id": patient_id,
    }


# -------------------- Prediction routes --------------------

@app.post("/predict/{patient_id}")
def predict_readmission(patient_id: int):
    """
    Get patient information from SQLite, apply the saved preprocessor,
    make a prediction, and save that prediction in SQLite.
    """
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT patient_data FROM patients WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Patient not found.")

        patient_data = json.loads(row[0])
        patient_frame = make_model_input(patient_data)

        try:
            processed_patient = preprocessor.transform(patient_frame)
            prediction = int(model.predict(processed_patient)[0])

            class_values = list(model.classes_)
            positive_index = class_values.index(1)
            probability = float(
                model.predict_proba(processed_patient)[0][positive_index]
            )
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not process this patient record. Check the entered "
                    "values and make sure they match the training data."
                ),
            ) from error

        cursor = connection.execute(
            """
            INSERT INTO predictions (patient_id, prediction, probability)
            VALUES (?, ?, ?)
            """,
            (patient_id, prediction, probability),
        )
        prediction_id = cursor.lastrowid
        connection.commit()

    if prediction == 1:
        result = "Readmitted within 30 days"
    else:
        result = "Not readmitted within 30 days"

    return {
        "prediction_id": prediction_id,
        "patient_id": patient_id,
        "model": MODEL_NAME,
        "prediction": prediction,
        "result": result,
        "readmission_probability": round(probability, 4),
    }


@app.get("/predictions")
def list_predictions():
    """Return prediction history for the dashboard and result page."""
    with closing(get_connection()) as connection:
        rows = connection.execute("""
            SELECT prediction_id, patient_id, prediction, probability
            FROM predictions
            ORDER BY prediction_id DESC
        """).fetchall()

    return [
        {
            "prediction_id": row[0],
            "patient_id": row[1],
            "prediction": row[2],
            "readmission_probability": round(float(row[3]), 4),
        }
        for row in rows
    ]


# -------------------- Dashboard and model information --------------------

@app.get("/stats")
def get_stats():
    """Return the values displayed in the CareLoop dashboard."""
    with closing(get_connection()) as connection:
        total_patients = connection.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]

        values = connection.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(prediction), 0),
                COALESCE(AVG(probability), 0)
            FROM predictions
        """).fetchone()

    return {
        "total_patients": total_patients,
        "total_predictions": values[0],
        "high_risk_predictions": int(values[1]),
        "average_probability": round(float(values[2]), 4),
    }


@app.get("/model-info")
def get_model_info():
    """Return the same comparison details displayed on the Model page."""
    if not MODEL_COMPARISON_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Model comparison information was not found.",
        )

    with MODEL_COMPARISON_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


# Serve the frontend from the same FastAPI address.
# Keep this mount after the API routes.
if FRONTEND_FOLDER.is_dir():
    app.mount(
        "/app",
        StaticFiles(directory=str(FRONTEND_FOLDER), html=True),
        name="frontend",
    )
