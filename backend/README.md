backend/README.md
# Healthcare Analytics – Backend (FastAPI)

This backend service provides REST APIs for healthcare analytics with a focus on **Health Insurance Fraud Detection** using machine learning.

---

## 🧰 Tech Stack

- Python 3.10+
- FastAPI
- Scikit-learn
- Uvicorn
- Pydantic
- Joblib

---

## 📁 Folder Structure



backend/
├── app/
│ ├── api/
│ │ └── v1/
│ │ ├── routers/
│ │ │ └── fraud_detection.py
│ │ └── schemas/
│ │ └── fraud_schema.py
│ ├── core/
│ │ └── model_loader.py
│ ├── utils/
│ │ └── preprocess.py
│ ├── ml_models/
│ │ └── fraud_model.pkl
│ └── main.py
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

🚀 Run the Backend Server

From the backend directory:

uvicorn app.main:app --reload

API Access

Swagger UI:
http://localhost:8000/docs

Fraud Prediction Endpoint:

POST /fraud/predict

📊 Model Details

Algorithm: RandomForest / XGBoost

Input validation: Pydantic schemas

Model file: fraud_model.pkl

⚠️ Common Issues

Ensure model file exists in ml_models/

Run uvicorn from the backend folder

Verify feature order matches training data

🏁 Notes

Designed for modular expansion

Supports future authentication & logging

Production-ready folder structure