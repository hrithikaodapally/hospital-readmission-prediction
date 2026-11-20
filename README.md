CareLoop – Hospital Readmission Risk Prediction

CareLoop is a Machine Learning-based application designed to predict the risk of hospital readmission. It helps care coordinators and healthcare professionals identify patients who may require additional attention and follow-up after discharge.

The project uses Machine Learning classification algorithms to analyse patient information and estimate the likelihood of readmission.

---

1. Project Objectives

- Predict the possibility of hospital readmission using Machine Learning.
- Identify patients who may require timely follow-up care.
- Compare different Machine Learning algorithms and select a suitable model.
- Store patient information and prediction results in a database.
- Provide a simple web application for interacting with the trained model.

2. Technologies Used

Component| Technologies
Programming Language| Python
Machine Learning| Scikit-learn
Data Processing| Pandas, NumPy
Model Training| Jupyter Notebook
Backend| FastAPI
Database| SQLite
Frontend| HTML, CSS, JavaScript
Model Saving| Joblib
API Testing| Postman
Public URL Generation| ngrok
Version Control| Git and GitHub

3. Machine Learning Models

Three classification algorithms were trained and evaluated using the preprocessed dataset.

1. Decision Tree Classifier
2. Logistic Regression
3. Random Forest Classifier

Model Comparison

The following results were obtained during the model evaluation:

Evaluation Metric| Decision Tree| Logistic Regression| Random Forest
Accuracy| 59.74%| 65.54%| 85.24%
Precision| 14.70%| 16.65%| 25.68%
Recall| 57.69%| 55.60%| 20.22%
F1 Score| 23.42%| 25.62%| 22.63%
ROC-AUC| 0.608| 0.656| 0.673

Selected Model: Logistic Regression

After comparing the three models, Logistic Regression was selected for backend integration because it achieved the highest F1 score among the evaluated models.

The selection considers the balance between precision and recall rather than accuracy alone.

The other two models are retained in the project for comparison.

4. Project Structure

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
│   └── model_comparison
│
├── examples/
│   └── Postman test files
│
├── requirements.txt
└── README.md

5. Application Workflow

1. The user enters patient information through the CareLoop frontend.
2. The FastAPI backend receives the information.
3. Patient details are stored in the SQLite database.
4. The backend retrieves the registered patient's information using the patient ID.
5. The selected Logistic Regression model processes the patient information.
6. The model generates a readmission prediction.
7. The prediction result is stored in the database.
8. The frontend displays the prediction to the user.

6. Database Design

CareLoop uses SQLite for storing patient information and prediction results.

The main database tables are:

Table| Purpose
Patients| Stores registered patient details
Predictions| Stores the predicted readmission results
Followups| Stores follow-up information

7. Installation and Setup

Step 1: Clone the repository

git clone https://github.com/hrithikaodapally/hospital-readmission-prediction.git

Step 2: Open the project folder

cd hospital-readmission-prediction

Step 3: Install dependencies

python -m pip install -r requirements.txt

Step 4: Start the FastAPI server

python -m uvicorn backend.main:app --reload

Step 5: Open the application

Application:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs

8. API Testing

The FastAPI endpoints can be tested using Postman.

- Select the POST method for prediction requests.
- Send patient information in JSON format.
- Verify that the API returns the prediction result.
- Confirm that patient details and prediction results are stored in the database.

9. Public URL Generation

The application can be made accessible over the internet using ngrok.

After starting the FastAPI server, execute:

ngrok http 8000

ngrok generates a public HTTPS URL that can be shared for application access and API testing.

The local server and ngrok tunnel must remain active while using the public URL.

10. Team Members

This project is developed by the following team members:

S. No.| GitHub Username
1| "hrithikaodapally" (https://github.com/hrithikaodapally)
2| "deekshithareddyshada" (https://github.com/deekshithareddyshada)
3| "swetchakasam.18" (https://github.com/swetchakasam.18)
4| "JAMANEERAJSAI" (https://github.com/JAMANEERAJSAI)

11. Conclusion

CareLoop combines Machine Learning, database management and web application development to build a hospital readmission risk prediction system.

By comparing multiple classification algorithms and integrating the selected model with a FastAPI backend, the project provides an application for generating and viewing patient readmission predictions.

Note: CareLoop is an academic prototype. Its predictions are not clinically validated and should not be used as a substitute for professional medical judgement.

---

Project Name: CareLoop
Project Domain: Healthcare and Machine Learning
Repository: https://github.com/hrithikaodapally/hospital-readmission-prediction