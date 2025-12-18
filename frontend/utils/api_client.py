import requests

API_BASE = "http://localhost:8000/api/v1"  # adjust for Docker or remote

def predict_fraud(payload: dict):
    url = f"{API_BASE}/fraud/predict"
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def get_metrics():
    url = f"{API_BASE}/fraud/metrics"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
