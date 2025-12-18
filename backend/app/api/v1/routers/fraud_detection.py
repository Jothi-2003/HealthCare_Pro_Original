from fastapi import APIRouter, HTTPException
import pandas as pd
from backend.app.core.model_loader import load_fraud_model
from backend.app.api.v1.schemas.fraud_schema import (
    FraudPredictRequest, FraudPredictResponse, FraudMetricsResponse
)
from pathlib import Path
import joblib
from app.core.config import settings


router = APIRouter(tags=["Fraud Detection"])
_model = None
_meta = {}

def _ensure_model():
    global _model
    if _model is None:
        _model = load_fraud_model()
    return _model

@router.post("/fraud/predict", response_model=FraudPredictResponse)
def predict_fraud(payload: FraudPredictRequest):
    model = _ensure_model()
    # Convert request to dataframe with one row
    data = pd.DataFrame([payload.model_dump()])
    # Drop non-feature identifiers if they were excluded during training
    if "claim_id" in data.columns:
        X = data.drop(columns=["claim_id"])
    else:
        X = data
    try:
        proba = float(model.predict_proba(X)[0][1])
        return FraudPredictResponse(
            claim_id=payload.claim_id,
            probability=proba,
            is_fraud=proba >= 0.5
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {str(e)}")

@router.get("/fraud/metrics", response_model=FraudMetricsResponse)
def fraud_metrics():
    # During training we store metrics sidecar next to model, or embed in model if desired.
    # For simplicity, return placeholders if metadata is absent.
    if not _meta:
        return FraudMetricsResponse(accuracy=0.0, auc=None)
    return FraudMetricsResponse(**_meta)
# After _model is prepared, load metrics
_metrics_loaded = False

def _load_metrics():
    global _meta, _metrics_loaded
    if _metrics_loaded:
        return
    sidecar = Path(settings.MODEL_PATH).with_suffix(".metrics.pkl")
    if sidecar.exists():
        _meta = joblib.load(sidecar)
    _metrics_loaded = True

# Call inside endpoints or at module import
_load_metrics()