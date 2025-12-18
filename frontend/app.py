import streamlit as st
from utils.api_client import predict_fraud, get_metrics
from utils.charts import probability_gauge

st.set_page_config(page_title="Health Insurance Fraud Detection", page_icon="🛡️", layout="centered")
# Header
col1, col2 = st.columns([1,4])
with col1:
    st.image("frontend/assets/images/fraud_icon.png", width=120)
with col2:
    st.title("Health Insurance Fraud Detection")
    st.write("Enter claim details to predict fraud probability.")

# Metrics
with st.expander("Model metrics"):
    try:
        m = get_metrics()
        st.metric("Accuracy", f"{m['accuracy']:.2f}")
        st.metric("AUC", f"{m['auc']:.2f}" if m['auc'] is not None else "NA")
    except Exception as e:
        st.info("Metrics unavailable. Train the model first.")

# Form
with st.form("fraud_form", clear_on_submit=False):
    st.subheader("Claim details")
    claim_id = st.text_input("Claim ID", value="CLM-0001")
    patient_age = st.number_input("Patient age", min_value=0, max_value=120, value=45)
    provider_id = st.text_input("Provider ID", value="PRV-123")
    claim_amount = st.number_input("Claim amount", min_value=0.0, value=15000.0, step=500.0)
    num_diagnoses = st.number_input("Number of diagnoses", min_value=0, value=2)
    num_procedures = st.number_input("Number of procedures", min_value=0, value=1)
    days_hospitalized = st.number_input("Days hospitalized", min_value=0, value=3)
    is_emergency = st.checkbox("Emergency case", value=False)
    out_of_network = st.checkbox("Out-of-network", value=False)
    previous_claims_count = st.number_input("Previous claims count", min_value=0, value=4)
    denied_claims_count = st.number_input("Denied claims count", min_value=0, value=1)

    submitted = st.form_submit_button("Predict fraud")

if submitted:
    payload = {
        "claim_id": claim_id,
        "patient_age": patient_age,
        "provider_id": provider_id,
        "claim_amount": claim_amount,
        "num_diagnoses": num_diagnoses,
        "num_procedures": num_procedures,
        "days_hospitalized": days_hospitalized,
        "is_emergency": is_emergency,
        "out_of_network": out_of_network,
        "previous_claims_count": previous_claims_count,
        "denied_claims_count": denied_claims_count,
    }
    try:
        result = predict_fraud(payload)
        probability_gauge(result["probability"])
        st.success(f"Fraud flag: {'Likely fraud' if result['is_fraud'] else 'Low risk'}")
        st.code(result, language="json")
    except Exception as e:
        st.error(f"Prediction failed: {e}")