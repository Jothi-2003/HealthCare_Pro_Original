import requests

API_BASE = "http://localhost:8000/api/v1"  # adjust for Docker or remote deployment

def predict_fraud(payload: dict) -> dict:
    """
    Send a fraud prediction request to the backend.

    Args:
        payload (dict): Claim data matching FraudPredictRequest schema.

    Returns:
        dict: JSON response with Claim_ID, probability, and is_fraud.
    """
    url = f"{API_BASE}/fraud/predict"
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Prediction request failed: {e}")

def get_metrics() -> dict:
    """
    Fetch model metrics (accuracy, AUC) from the backend.

    Returns:
        dict: JSON response with accuracy and auc.
    """
    url = f"{API_BASE}/fraud/metrics"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Metrics request failed: {e}")