🏥 CareLoop

Hospital Readmission Risk Prediction System

Predict early. Follow up better. Care beyond discharge.

CareLoop is a Machine Learning-based hospital readmission prediction system that helps identify patients who may be at risk of returning to the hospital after discharge.

The application uses patient information to generate readmission risk predictions, helping care coordinators and healthcare professionals prioritize follow-up care.

---

📌 Overview

Hospital readmissions can increase healthcare costs and create additional challenges for patients, families and hospitals.

CareLoop aims to address this problem by using Machine Learning to analyse patient data and predict the possibility of readmission.

The system combines a trained ML model, a database and a web application to provide a simple way to register patients, generate predictions and view results.

✨ Key Features

- Patient Registration: Enter and store patient information in the database.
- Readmission Prediction: Predict the possibility of hospital readmission using a trained Machine Learning model.
- Model Comparison: Evaluate Decision Tree, Logistic Regression and Random Forest classifiers.
- Risk Assessment: Display the model's predicted outcome and probability.
- Patient Records: Maintain registered patient information.
- Prediction History: Store and retrieve previous prediction results.
- Web Dashboard: View patient and prediction information through a user-friendly interface.

🧠 Machine Learning Approach

We experimented with three classification algorithms using the same preprocessed training and testing datasets.

Model| Accuracy| Precision| Recall| F1 Score
Decision Tree| 59.74%| 14.70%| 57.69%| 23.42%
Logistic Regression| 65.54%| 16.65%| 55.60%| 25.62%
Random Forest| 85.24%| 25.68%| 20.22%| 22.63%

Model Selection

After comparing the evaluation results, Logistic Regression was selected for backend integration because it achieved the highest F1 score among the three models.

The models were compared using accuracy, precision, recall, F1 score and ROC-AUC. We considered more than accuracy alone when selecting the model.

All three model training notebooks and their evaluation results are maintained in the "models/" directory.

⚙️ Technology Stack

Area| Technologies
Programming Language| Python
Data Processing| Pandas, NumPy
Machine Learning| Scikit-learn
Model Development| Jupyter Notebook
Model Storage| Joblib
Backend| FastAPI
Database| SQLite
Frontend| HTML, CSS, JavaScript
API Testing| Postman
Public Access| ngrok
Version Control| Git, GitHub

🔄 How CareLoop Works

        PATIENT REGISTRATION
                 |
                 v
        Enter Patient Details
                 |
                 v
          FASTAPI BACKEND
                 |
                 v
          SQLITE DATABASE
        (Save Patient Details)
                 |
                 v
       Retrieve Patient Record
                 |
                 v
       PREPROCESSING PIPELINE
                 |
                 v
       LOGISTIC REGRESSION
                 |
                 v
        READMISSION PREDICTION
                 |
                 v
       Save Prediction in Database
                 |
                 v
          CARELOOP DASHBOARD
                 |
                 v
           Display Result

📂 Project Structure

CareLoop/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   └── routes/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── pages/
│
├── preprocessing/
│   └── data_preprocessing.ipynb
│
├── models/
│   ├── decision_tree/
│   │   ├── decision_tree_training.ipynb
│   │   ├── model.joblib
│   │   └── metrics.json
│   │
│   ├── logistic_regression/
│   │   ├── logistic_regression_training.ipynb
│   │   ├── model.joblib
│   │   └── metrics.json
│   │
│   └── random_forest/
│       ├── random_forest_training.ipynb
│       ├── model.joblib
│       └── metrics.json
│
├── evaluation/
├── examples/
├── requirements.txt
└── README.md

🚀 Getting Started

Follow these steps to run CareLoop on your local machine.

Prerequisites

- Python installed on your system
- Visual Studio Code
- Git
- Required Python libraries

1. Clone the repository

git clone https://github.com/hrithikaodapally/hospital-readmission-prediction.git

2. Navigate to the project folder

cd hospital-readmission-prediction

3. Install the required libraries

python -m pip install -r requirements.txt

4. Start the FastAPI server

python -m uvicorn backend.main:app --reload

5. Open CareLoop

Application:

http://127.0.0.1:8000

FastAPI API Documentation:

http://127.0.0.1:8000/docs

The API documentation can be used to inspect and test the available endpoints.

🧪 API Testing

The backend APIs can be tested using Postman.

The testing process includes:

1. Registering a patient.
2. Checking whether the patient information is saved in SQLite.
3. Sending a prediction request for the registered patient.
4. Checking the returned prediction and probability.
5. Verifying that the prediction is stored in the database.

🌐 Public Access Using ngrok

CareLoop can be made accessible over the internet using ngrok.

Once the local FastAPI server is running, execute:

ngrok http 8000

ngrok generates a public HTTPS URL that can be shared for accessing the running application and API documentation.

The local backend and ngrok tunnel must remain active while the public URL is being used.

👥 Project Team

Developed as part of the Student Development Cell (SDC) Project.

Team Member| GitHub
Hrithika Odapally| "@hrithikaodapally" (https://github.com/hrithikaodapally)
Deekshitha Reddy Shada| "@deekshithareddyshada" (https://github.com/deekshithareddyshada)
Swetcha Kasam| "swetchakasam.18"
Neeraj Sai| "@JAMANEERAJSAI" (https://github.com/JAMANEERAJSAI)

🎯 Project Goal

Our goal with CareLoop is to demonstrate how Machine Learning can be integrated into a practical healthcare application to support early identification of patients who may need additional attention after hospital discharge.

---

⚠️ Disclaimer

CareLoop is an academic project developed for educational purposes. Its predictions are based on the available dataset and have not been clinically validated. It is not intended for actual medical diagnosis or treatment decisions.

---

CareLoop | Predict Early. Follow Up Better.