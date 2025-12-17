from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # points to healthcare_analytics/
DATASETS_DIR = BASE_DIR / "datasets"

# Update this if you use a different filename
FRAUD_DATA_PATH = DATASETS_DIR / "fraud_claims.csv"

MODELS_DIR = BASE_DIR / "backend" / "app" / "ml_models"
FRAUD_MODEL_PATH = MODELS_DIR / "fraud_model.pkl"
FRAUD_METRICS_PATH = MODELS_DIR / "fraud_metrics.json"