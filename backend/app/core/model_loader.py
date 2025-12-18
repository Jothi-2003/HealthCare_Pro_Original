import joblib
from pathlib import Path
from .config import settings

def load_fraud_model():
    path = Path(settings.MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found at: {path.resolve()}")
    try:
        return joblib.load(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model at {path.resolve()}: {str(e)}")