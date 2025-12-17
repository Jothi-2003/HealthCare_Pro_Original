import streamlit as st
from frontend.utils.api_client import predict_fraud, get_fraud_metrics

st.header("Health Insurance Fraud Detection")

with st.form("fraud_form", clear_on_submit=False):
    claim_amount = st.number_input("Claim Amount", min_value=0.0, step=100.0)
    patient_age = st.number_input("Patient Age", min_value=0, max_value=120, step=1)
    days_since_last_claim = st.number_input("Days Since Last Claim", min_value=0, step=1)
    num_diagnoses = st.number_input("Number of Diagnoses", min_value=0, step=1)

    provider_id = st.text_input("Provider ID")
    procedure_code = st.text_input("Procedure Code")
    state = st.text_input("State")
    is_emergency = st.selectbox("Emergency?", options=["no", "yes"])

    submitted = st.form_submit_button("Predict Fraud")

    if submitted:
        payload = {
            "claim_amount": claim_amount,
            "patient_age": patient_age,
            "days_since_last_claim": days_since_last_claim,
            "num_diagnoses": num_diagnoses,
            "provider_id": provider_id,
            "procedure_code": procedure_code,
            "state": state,
            "is_emergency": is_emergency,
        }
        try:
            result = predict_fraud(payload)
            st.metric("Fraud Probability", f"{result['fraud_probability']:.2%}")
            st.success("Flagged as Fraud" if result["is_fraud"] else "Not Fraud")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.subheader("Model Metrics")
try:
    metrics = get_fraud_metrics()
    st.write(metrics)
except Exception as e:
    st.warning("Metrics unavailable. Train the model first.")