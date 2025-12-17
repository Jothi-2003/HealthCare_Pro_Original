# backend/app/api/v1/routers/fraud_detection.py
from fastapi import APIRouter
import pandas as pd
from ..schemas.fraud_schema import FraudClaimInput, FraudPredictionOutput
from ....core.model_loader import get_fraud_model, get_fraud_metrics

router = APIRouter(prefix="/fraud", tags=["Fraud"])

@router.post("/predict", response_model=FraudPredictionOutput)
def predict_fraud(payload: FraudClaimInput):
    bundle = get_fraud_model()
    pipeline = bundle["pipeline"]
    features = bundle["features"]

    # Construct a single-row DataFrame with exact training order
    data = {
        **{k: getattr(payload, k) for k in features["numeric"]},
        **{k: getattr(payload, k) for k in features["categorical"]},
    }
    X = pd.DataFrame([data])

    proba = float(pipeline.predict_proba(X)[:, 1][0])
    is_fraud = proba >= 0.5  # threshold configurable

    return FraudPredictionOutput(
        fraud_probability=round(proba, 4),
        is_fraud=bool(is_fraud),
        model_version="fraud_rf_v1"
    )

@router.get("/metrics")
def get_metrics():
    return get_fraud_metrics()