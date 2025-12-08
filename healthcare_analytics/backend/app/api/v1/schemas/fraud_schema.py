# backend/app/api/v1/schemas/fraud_schema.py
from pydantic import BaseModel, conint, confloat, Field
from typing import Literal

class FraudClaimInput(BaseModel):
    # Numeric
    claim_amount: confloat(ge=0)
    patient_age: conint(ge=0, le=120)
    days_in_hospital: conint(ge=0)
    num_procedures: conint(ge=0)
    prior_claims: conint(ge=0)
    billing_code_count: conint(ge=0)

    # Categorical (strings or booleans mapped to strings)
    provider_id: str
    procedure_code: str
    diagnosis_code: str
    is_in_network: Literal["yes", "no"]  # keep consistent with training

class FraudPredictionOutput(BaseModel):
    fraud_probability: float
    is_fraud: bool
    model_version: str = Field(default="fraud_rf_v1", const=True)