# backend/app/core/model_loader.py
import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/app
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "fraud_model.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "ml_models", "fraud_metrics.json")

_fraud_bundle = None
_fraud_metrics = None

def get_fraud_model():
    global _fraud_bundle
    if _fraud_bundle is None:
        _fraud_bundle = joblib.load(MODEL_PATH)
    return _fraud_bundle

def get_fraud_metrics():
    global _fraud_metrics
    if _fraud_metrics is None:
        import json
        with open(METRICS_PATH, "r") as f:
            _fraud_metrics = json.load(f)
    return _fraud_metrics