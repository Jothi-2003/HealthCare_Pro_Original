import requests

BASE_URL = "http://localhost:8000/api/v1"

def predict_fraud(payload: dict):
    url = f"{BASE_URL}/fraud/predict"
    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()

def get_metrics():
    url = f"{BASE_URL}/fraud/metrics"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()