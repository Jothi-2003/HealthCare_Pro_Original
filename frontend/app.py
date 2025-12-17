# frontend/app.py
import json
import requests
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Fraud Detector", page_icon="🛡️", layout="centered")
st.title("Health Insurance Fraud Detection")

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000/api/v1")
FEATURES_LOCAL = Path("../backend/app/ml_models/fraud_feature_names.json")  # adjust if needed

def load_features():
    if FEATURES_LOCAL.exists():
        with open(FEATURES_LOCAL, "r") as f:
            return json.load(f)
    st.warning("Feature names file not found locally. You can still submit custom keys.")
    return {"all_features": []}

feat_info = load_features()
features = feat_info.get("all_features", [])

with st.form("fraud_form"):
    st.subheader("Enter claim details")
    inputs = {}
    for f in features:
        # simple heuristic: numeric vs categorical by name
        if any(k in f.lower() for k in ["amount", "age", "days", "count", "num", "cost"]):
            val = st.number_input(f, value=0.0, step=100.0, format="%.2f")
        else:
            val = st.text_input(f, value="")
        inputs[f] = val if val != "" else None
    # If no features known, allow manual JSON
    manual_json = st.text_area("Or paste JSON features", value="", help='Example: {"claim_amount": 12000, "region": "South"}')
    submitted = st.form_submit_button("Predict fraud")

if submitted:
    payload = {"features": inputs}
    if manual_json.strip():
        try:
            manual = json.loads(manual_json)
            payload = {"features": manual}
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

    try:
        r = requests.post(f"{API_BASE}/fraud/predict", json=payload, timeout=10)
        if r.status_code == 200:
            res = r.json()
            st.metric("Fraud probability", f"{res['fraud_probability']:.2f}")
            if res["is_fraud"]:
                st.error("Flag: FRAUD")
            else:
                st.success("Flag: NOT FRAUD")
        else:
            st.error(f"API error {r.status_code}: {r.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()
st.subheader("Model metrics")
if st.button("Fetch metrics"):
    try:
        r = requests.get(f"{API_BASE}/fraud/metrics", timeout=10)
        if r.status_code == 200:
            m = r.json()
            cols = st.columns(5)
            cols[0].metric("Accuracy", f"{m['accuracy']:.3f}")
            cols[1].metric("Precision", f"{m['precision']:.3f}")
            cols[2].metric("Recall", f"{m['recall']:.3f}")
            cols[3].metric("F1", f"{m['f1']:.3f}")
            roc = m.get("roc_auc")
            cols[4].metric("ROC-AUC", f"{roc:.3f}" if roc is not None else "N/A")
        else:
            st.error(f"API error {r.status_code}: {r.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")