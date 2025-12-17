import requests

API_BASE = "http://localhost:8000"  # adjust for Docker or remote

def predict_fraud(payload: dict):
    url = f"{API_BASE}/fraud/predict"
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def get_fraud_metrics():
    url = f"{API_BASE}/fraud/metrics"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()