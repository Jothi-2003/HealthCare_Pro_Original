from pydantic import BaseModel, Field

class FraudClaimInput(BaseModel):
    claim_amount: float = Field(..., ge=0)
    patient_age: int = Field(..., ge=0, le=120)
    days_since_last_claim: int = Field(..., ge=0)
    num_diagnoses: int = Field(..., ge=0)

    provider_id: str
    procedure_code: str
    state: str
    is_emergency: str  # e.g., "yes"/"no" or "true"/"false"

class FraudPredictionOutput(BaseModel):
    fraud_probability: float
    is_fraud: bool