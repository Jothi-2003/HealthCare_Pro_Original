# db/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean
from db.database import Base

class FraudClaim(Base):
    __tablename__ = "fraud_claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_amount = Column(Float)
    provider_id = Column(String)
    patient_age = Column(Integer)
    procedure_code = Column(String)
    diagnosis_code = Column(String)
    hospital_type = Column(String)
    days_admitted = Column(Integer)
    previous_claims_count = Column(Integer)
    region = Column(String)
    is_fraud = Column(Boolean)