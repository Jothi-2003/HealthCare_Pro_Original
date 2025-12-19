# Healthcare Insurance Fraud Detection – Project Flow

This document explains the complete end-to-end workflow of the Healthcare Insurance Fraud Detection system.

---

## 🔄 Overall System Flow

The project follows a modular and layered architecture, integrating Machine Learning, FastAPI, and Streamlit.

---

## 1️⃣ Data Collection & Preparation

- Dataset location:
datasets/fraud_claims.csv

yaml
Copy code
- The dataset contains historical health insurance claim records.
- Includes both fraudulent and genuine claims.
- Data preprocessing includes:
- Handling missing values
- Encoding categorical features
- Feature selection

---

## 2️⃣ Model Training

- Training script:
train_fraud_model.py


- Machine Learning algorithms used:
- Random Forest
- XGBoost (optional)
- Output files:
backend/app/ml_models/fraud_model.pkl
backend/app/ml_models/metrics.pkl


- Model evaluation metrics:
- Accuracy
- Precision
- Recall
- F1-score

---

## 3️⃣ Backend Development (FastAPI)

- Entry point:
backend/app/main.py


- Responsibilities:
- Load trained ML model at startup
- Register API routers
- Handle request validation and responses

---

## 4️⃣ API Layer – Fraud Detection

- Router file:
backend/app/api/v1/routers/fraud_detection.py

- API Endpoint:
POST /fraud/predict


- Flow:
- Receives JSON request
- Validates input using Pydantic schema
- Preprocesses input data
- Sends data to ML model for prediction
- Returns fraud probability and decision

---

## 5️⃣ Business Logic & Preprocessing

- Preprocessing utility:
backend/app/utils/preprocess.py

- Tasks:
- Feature encoding
- Data type conversion
- Feature ordering to match training data

---

## 6️⃣ Frontend Integration (Streamlit)

- Frontend entry:
frontend/app.py

- Responsibilities:
- Collect claim details from user
- Send POST request to backend API
- Receive prediction response
- Display results visually

---

## 7️⃣ API Communication

- API client:
frontend/utils/api_client.py


- Communication:
Streamlit UI → FastAPI → ML Model → FastAPI → Streamlit UI


---

## 8️⃣ Result Visualization

- Displays:
- Fraud probability
- Fraud / Genuine classification
- Optional visual components:
frontend/utils/charts.py


---

## 🔗 System Connectivity Diagram

[User]
↓
[Streamlit Frontend]
↓
[FastAPI Backend]
↓
[Fraud Detection Model]
↓
[Prediction Response]
↓
[Frontend Display]


---

## 🧩 Optional Enhancements

- Authentication using JWT
- Database logging of predictions
- Role-based access control
- Model versioning and monitoring

---

## ✅ Best Practices Followed

- Clear separation of concerns
- Modular folder structure
- Input validation using Pydantic
- Reusable preprocessing logic
- Scalable API design

---

## 🏁 Conclusion

This project demonstrates a complete ML-powered web application, covering data processing, model training, API deploym