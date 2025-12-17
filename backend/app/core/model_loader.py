# backend/app/core/model_loader.py
import json
import joblib
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

ML_DIR = Path(__file__).resolve().parent.parent / "ml_models"
MODEL_PATH = ML_DIR / "fraud_model.pkl"
METRICS_PATH = ML_DIR / "fraud_metrics.json"
FEATURES_PATH = ML_DIR / "fraud_feature_names.json"

_model = None
_metrics = None
_features = None

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model

def get_metrics() -> Optional[dict]:
    global _metrics
    if _metrics is None:
        if not METRICS_PATH.exists():
            return None
        with open(METRICS_PATH, "r") as f:
            _metrics = json.load(f)
    return _metrics

def get_feature_names() -> Dict[str, Any]:
    global _features
    if _features is None:
        if not FEATURES_PATH.exists():
            raise FileNotFoundError(f"Feature names not found at {FEATURES_PATH}")
        with open(FEATURES_PATH, "r") as f:
            _features = json.load(f)
    return _features

def align_payload_to_features(payload: Dict[str, Any]) -> pd.DataFrame:
    """Ensure incoming JSON is aligned to trained feature order, filling missing with None."""
    features = get_feature_names()["all_features"]
    row = {k: payload.get(k, None) for k in features}
    return pd.DataFrame([row], columns=features)