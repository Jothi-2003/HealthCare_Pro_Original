---

## 📄 `frontend/README.md`

```md
# Healthcare Analytics – Frontend (Streamlit)

This frontend provides an interactive UI for **Health Insurance Fraud Detection**, built using Streamlit.

---

## 🧰 Tech Stack

- Python 3.10+
- Streamlit
- Requests
- Matplotlib / Plotly (optional)

---

## 📁 Folder Structure

frontend/
├── app.py
├── utils/
│ ├── api_client.py
│ └── charts.py
├── assets/
│ ├── styles.css
│ └── images/
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
🚀 Run the Frontend App
From the frontend directory:

streamlit run app.py
🔗 Backend Connectivity
Backend must be running at:


http://localhost:8000
API used:

POST /fraud/predict
🎯 Features
Claim data input form

Fraud probability prediction

Fraud / Genuine status indicator

Clean and simple UI

⚠️ Common Issues
Start backend before frontend

Check API URL in api_client.py

Ensure ports 8000 and 8501 are free

🏁 Notes
Designed as a single-page application

Easily extendable for multiple ML models

Suitable for demos, viva, and presentations
