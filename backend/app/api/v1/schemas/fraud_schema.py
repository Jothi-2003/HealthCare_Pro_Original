# backend/app/api/v1/schemas/fraud_schema.py
from pydantic import BaseModel
from typing import Dict, Any, Optional

class FraudClaimInput(BaseModel):
    # Free-form feature map; keys should match CSV feature names
    features: Dict[str, Any]

class FraudPredictionOutput(BaseModel):
    fraud_probability: float
    is_fraud: bool

class FraudMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: Optional[float]  # Use Optional for compatibility across Python versions