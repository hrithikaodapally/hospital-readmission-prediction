@echo off
 title CareLoop - Hospital Readmission Prediction
 python -m uvicorn backend.main:app --reload
 pause
