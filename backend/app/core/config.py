# core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Healthcare Analytics"
    API_PREFIX: str = "/api/v1"
    MODEL_DIR: str = "app/ml_models"

settings = Settings()