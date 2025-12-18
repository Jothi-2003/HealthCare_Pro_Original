from pydantic import BaseModel, Field

class FraudPredictRequest(BaseModel):
    claim_id: str = Field(..., description="Unique claim identifier")
    patient_age: int = Field(..., ge=0, le=120)
    provider_id: str = Field(..., description="Provider identifier")
    claim_amount: float = Field(..., ge=0)
    num_diagnoses: int = Field(..., ge=0)
    num_procedures: int = Field(..., ge=0)
    days_hospitalized: int = Field(..., ge=0)
    is_emergency: bool = Field(..., description="Emergency claim")
    out_of_network: bool = Field(..., description="Out-of-network service")
    previous_claims_count: int = Field(..., ge=0)
    denied_claims_count: int = Field(..., ge=0)
    # Add/adjust fields to match your CSV exactly

class FraudPredictResponse(BaseModel):
    claim_id: str
    probability: float
    is_fraud: bool

class FraudMetricsResponse(BaseModel):
    accuracy: float
    auc: float | None = None

class FraudRequest(BaseModel):
    denied_claims: int