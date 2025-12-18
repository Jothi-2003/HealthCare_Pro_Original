import joblib
from pathlib import Path
from .config import settings

def load_fraud_model(model_path: str | None = None):
    path = Path(model_path or settings.MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at: {path.resolve()}")
    return joblib.load(path)