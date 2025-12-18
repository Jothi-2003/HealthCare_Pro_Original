from pydantic import BaseModel
import os

class Settings(BaseModel):
    MODEL_PATH: str = os.getenv("FRAUD_MODEL_PATH", "backend/app/ml_models/fraud_model.pkl")
    TARGET_COLUMN: str = os.getenv("FRAUD_TARGET_COLUMN", "is_fraud")

settings = Settings()