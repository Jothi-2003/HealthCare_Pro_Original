from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "backend/app/ml_models/fraud_model.pkl"
    TARGET_COLUMN: str = "Is_Fraudulent"

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()