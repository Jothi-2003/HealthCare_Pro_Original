# Healthcare Insurance Fraud Detection – API Documentation

## 🔌 API Overview

- **Base URL:** http://localhost:8000
- **Service:** Healthcare Analytics – Fraud Detection
- **Protocol:** REST (JSON)

---

## 🚀 Fraud Prediction Endpoint

### Endpoint
POST /fraud/predict

### Description
Predicts whether a health insurance claim is fraudulent based on claim details.

---

## 📦 Request Schema

Defined in `fraud_schema.py`.

| Field Name | Type | Description |
|-----------|------|-------------|
| claim_amount | float | Total claim amount |
| patient_age | integer | Age of the patient |
| days_in_hospital | integer | Hospital stay duration |
| num_procedures | integer | Number of procedures |
| prior_claims | integer | Previous claims count |
| provider_fraud_history | integer (0/1) | Provider fraud history |
| claim_type | string | cashless / reimbursement |

---

## 📤 Sample Request

```json
{
  "claim_amount": 120000,
  "patient_age": 45,
  "days_in_hospital": 5,
  "num_procedures": 2,
  "prior_claims": 1,
  "provider_fraud_history": 0,
  "claim_type": "cashless"
}
