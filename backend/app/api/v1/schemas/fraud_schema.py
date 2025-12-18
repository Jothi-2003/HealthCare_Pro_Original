from pydantic import BaseModel, Field
from typing import Optional

class FraudPredictRequest(BaseModel):
    Patient_ID: str = Field(..., description="Unique patient identifier")
    Policy_Number: str = Field(..., description="Policy number")
    Claim_ID: str = Field(..., description="Unique claim identifier")
    Claim_Date: str = Field(..., description="Date of claim submission (string or ISO date)")
    Service_Date: str = Field(..., description="Date of service (string or ISO date)")
    Policy_Expiration_Date: str = Field(..., description="Policy expiration date (string or ISO date)")
    Claim_Amount: float = Field(..., ge=0)
    Patient_Age: int = Field(..., ge=0, le=120)
    Patient_Gender: str
    Patient_City: str
    Patient_State: str
    Hospital_ID: str
    Provider_Type: str
    Provider_Specialty: str
    Provider_City: str
    Provider_State: str
    Diagnosis_Code: str
    Procedure_Code: str
    Number_of_Procedures: int = Field(..., ge=0)
    Admission_Type: str
    Discharge_Type: str
    Length_of_Stay_Days: int = Field(..., ge=0)
    Service_Type: str
    Deductible_Amount: float = Field(..., ge=0)
    CoPay_Amount: float = Field(..., ge=0)
    Number_of_Previous_Claims_Patient: int = Field(..., ge=0)
    Number_of_Previous_Claims_Provider: int = Field(..., ge=0)
    Provider_Patient_Distance_Miles: float = Field(..., ge=0)
    Claim_Submitted_Late: bool
    Is_Fraudulent: Optional[int] = None  # present only in dataset, not required for inference

    class Config:
        json_schema_extra = {
            "example": {
                "Patient_ID": "P001",
                "Policy_Number": "POL123",
                "Claim_ID": "CLM001",
                "Claim_Date": "2025-01-10",
                "Service_Date": "2025-01-08",
                "Policy_Expiration_Date": "2026-01-10",
                "Claim_Amount": 55000.0,
                "Patient_Age": 45,
                "Patient_Gender": "M",
                "Patient_City": "Chennai",
                "Patient_State": "TN",
                "Hospital_ID": "H123",
                "Provider_Type": "Hospital",
                "Provider_Specialty": "General",
                "Provider_City": "Chennai",
                "Provider_State": "TN",
                "Diagnosis_Code": "D001",
                "Procedure_Code": "PR001",
                "Number_of_Procedures": 2,
                "Admission_Type": "Emergency",
                "Discharge_Type": "Routine",
                "Length_of_Stay_Days": 3,
                "Service_Type": "Inpatient",
                "Deductible_Amount": 5000.0,
                "CoPay_Amount": 500.0,
                "Number_of_Previous_Claims_Patient": 1,
                "Number_of_Previous_Claims_Provider": 5,
                "Provider_Patient_Distance_Miles": 12.5,
                "Claim_Submitted_Late": False
            }
        }

class FraudPredictResponse(BaseModel):
    Claim_ID: str
    probability: float
    is_fraud: bool

class FraudMetricsResponse(BaseModel):
    accuracy: float
    auc: Optional[float] = None