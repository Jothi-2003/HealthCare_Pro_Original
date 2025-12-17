# db/seeds.py
import pandas as pd
from db.database import SessionLocal, engine, Base
from db.models import FraudClaim

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

def seed_from_csv(csv_path: str):
    df = pd.read_csv(csv_path)

    # Adjust column names to match your CSV
    # Example assumes columns: claim_amount, provider_id, patient_age, procedure_code, diagnosis_code, hospital_type, days_admitted, previous_claims_count, region, is_fraud
    session = SessionLocal()
    try:
        for _, row in df.iterrows():
            claim = FraudClaim(
                claim_amount=row.get("claim_amount"),
                provider_id=row.get("provider_id"),
                patient_age=row.get("patient_age"),
                procedure_code=row.get("procedure_code"),
                diagnosis_code=row.get("diagnosis_code"),
                hospital_type=row.get("hospital_type"),
                days_admitted=row.get("days_admitted"),
                previous_claims_count=row.get("previous_claims_count"),
                region=row.get("region"),
                is_fraud=bool(row.get("is_fraud")),
            )
            session.add(claim)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    seed_from_csv("datasets/fraud_claims.csv")
    print("Database seeded with fraud claims!")