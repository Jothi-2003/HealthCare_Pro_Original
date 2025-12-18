from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path
import joblib

from backend.app.core.model_loader import load_fraud_model
from backend.app.api.v1.schemas.fraud_schema import (
    FraudPredictRequest,
    FraudPredictResponse,
    FraudMetricsResponse,
)
from backend.app.core.config import settings

router = APIRouter(tags=["Fraud Detection"])

_model = None
_meta = {}
_metrics_loaded = False

IDENTIFIER_COLS = [
    "Claim_ID", "Patient_ID", "Policy_Number", "Hospital_ID"
]

def _ensure_model():
    global _model
    if _model is None:
        try:
            _model = load_fraud_model()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model load error: {str(e)}")
    return _model

def _load_metrics():
    global _meta, _metrics_loaded
    if _metrics_loaded:
        return
    sidecar = Path(settings.MODEL_PATH).with_suffix(".metrics.pkl")
    if sidecar.exists():
        try:
            _meta = joblib.load(sidecar)
        except Exception:
            _meta = {}
    _metrics_loaded = True

@router.post("/fraud/predict", response_model=FraudPredictResponse)
def predict_fraud(payload: FraudPredictRequest):
    model = _ensure_model()
    data = pd.DataFrame([payload.model_dump()])

    # Drop identifiers
    drop_cols = [c for c in IDENTIFIER_COLS if c in data.columns]
    X = data.drop(columns=drop_cols) if drop_cols else data

    try:
        proba = float(model.predict_proba(X)[0][1])
        return FraudPredictResponse(
            Claim_ID=payload.Claim_ID,
            probability=proba,
            is_fraud=proba >= 0.5,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {str(e)}")

@router.get("/fraud/metrics", response_model=FraudMetricsResponse)
def fraud_metrics():
    _load_metrics()
    if not _meta:
        return FraudMetricsResponse(accuracy=0.0, auc=None)
    return FraudMetricsResponse(**_meta)