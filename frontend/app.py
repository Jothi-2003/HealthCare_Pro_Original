import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1/fraud/predict"
METRICS_URL = "http://127.0.0.1:8000/api/v1/fraud/metrics"

st.set_page_config(page_title="Healthcare Fraud Detection", layout="wide")

st.title("🏥 Healthcare Claim Fraud Detection")

with st.form("fraud_form"):
    st.subheader("Enter Claim Details")

    Claim_ID = st.text_input("Claim ID")
    Patient_ID = st.text_input("Patient ID")
    Policy_Number = st.text_input("Policy Number")
    Claim_Date = st.date_input("Claim Date")
    Service_Date = st.date_input("Service Date")
    Policy_Expiration_Date = st.date_input("Policy Expiration Date")
    Claim_Amount = st.number_input("Claim Amount", min_value=0.0)
    Patient_Age = st.number_input("Patient Age", min_value=0, max_value=120)
    Patient_Gender = st.selectbox("Patient Gender", ["M", "F"])
    Patient_City = st.text_input("Patient City")
    Patient_State = st.text_input("Patient State")
    Hospital_ID = st.text_input("Hospital ID")
    Provider_Type = st.text_input("Provider Type")
    Provider_Specialty = st.text_input("Provider Specialty")
    Provider_City = st.text_input("Provider City")
    Provider_State = st.text_input("Provider State")
    Diagnosis_Code = st.text_input("Diagnosis Code")
    Procedure_Code = st.text_input("Procedure Code")
    Number_of_Procedures = st.number_input("Number of Procedures", min_value=0)
    Admission_Type = st.text_input("Admission Type")
    Discharge_Type = st.text_input("Discharge Type")
    Length_of_Stay_Days = st.number_input("Length of Stay (Days)", min_value=0)
    Service_Type = st.text_input("Service Type")
    Deductible_Amount = st.number_input("Deductible Amount", min_value=0.0)
    CoPay_Amount = st.number_input("CoPay Amount", min_value=0.0)
    Number_of_Previous_Claims_Patient = st.number_input("Previous Claims (Patient)", min_value=0)
    Number_of_Previous_Claims_Provider = st.number_input("Previous Claims (Provider)", min_value=0)
    Provider_Patient_Distance_Miles = st.number_input("Provider-Patient Distance (Miles)", min_value=0.0)
    Claim_Submitted_Late = st.checkbox("Claim Submitted Late")

    submitted = st.form_submit_button("🔍 Predict Fraud")

if submitted:
    payload = {
        "Patient_ID": Patient_ID,
        "Policy_Number": Policy_Number,
        "Claim_ID": Claim_ID,
        "Claim_Date": str(Claim_Date),
        "Service_Date": str(Service_Date),
        "Policy_Expiration_Date": str(Policy_Expiration_Date),
        "Claim_Amount": Claim_Amount,
        "Patient_Age": Patient_Age,
        "Patient_Gender": Patient_Gender,
        "Patient_City": Patient_City,
        "Patient_State": Patient_State,
        "Hospital_ID": Hospital_ID,
        "Provider_Type": Provider_Type,
        "Provider_Specialty": Provider_Specialty,
        "Provider_City": Provider_City,
        "Provider_State": Provider_State,
        "Diagnosis_Code": Diagnosis_Code,
        "Procedure_Code": Procedure_Code,
        "Number_of_Procedures": Number_of_Procedures,
        "Admission_Type": Admission_Type,
        "Discharge_Type": Discharge_Type,
        "Length_of_Stay_Days": Length_of_Stay_Days,
        "Service_Type": Service_Type,
        "Deductible_Amount": Deductible_Amount,
        "CoPay_Amount": CoPay_Amount,
        "Number_of_Previous_Claims_Patient": Number_of_Previous_Claims_Patient,
        "Number_of_Previous_Claims_Provider": Number_of_Previous_Claims_Provider,
        "Provider_Patient_Distance_Miles": Provider_Patient_Distance_Miles,
        "Claim_Submitted_Late": Claim_Submitted_Late
    }

    try:
        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            result = res.json()
            st.success(f"✅ Prediction complete for Claim {result['Claim_ID']}")
            st.metric("Fraud Probability", f"{result['probability']:.3f}")
            st.metric("Is Fraud?", "🚨 Yes" if result["is_fraud"] else "✅ No")
        else:
            st.error(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()
st.subheader("📊 Model Metrics")

try:
    metrics_res = requests.get(METRICS_URL)
    if metrics_res.status_code == 200:
        metrics = metrics_res.json()
        st.metric("Accuracy", f"{metrics['accuracy']:.3f}")
        st.metric("AUC", metrics['auc'] if metrics['auc'] is not None else "NA")
    else:
        st.warning("Metrics not available.")
except Exception as e:
    st.error(f"Failed to fetch metrics: {e}")