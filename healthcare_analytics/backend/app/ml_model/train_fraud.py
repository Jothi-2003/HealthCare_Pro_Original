# backend/app/ml_models/train_fraud.py
import json
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "datasets", "fraud_claims.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__))  # backend/app/ml_models
MODEL_PATH = os.path.join(MODEL_DIR, "fraud_model.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "fraud_metrics.json")

# Adjust these lists to match your dataset
NUMERIC_FEATURES = [
    "claim_amount", "patient_age", "days_in_hospital",
    "num_procedures", "prior_claims", "billing_code_count"
]
CATEGORICAL_FEATURES = [
    "provider_id", "procedure_code", "diagnosis_code", "is_in_network"
]
TARGET = "is_fraud"

def load_data():
    df = pd.read_csv(DATA_PATH)
    # Basic cleanup: drop rows missing critical fields
    df = df.dropna(subset=NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET])
    return df

def build_pipeline():
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    clf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"  # helps with imbalance
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("clf", clf),
    ])
    return pipeline

def main():
    df = load_data()
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    # Predictions for metrics
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred)), 4),
        "recall": round(float(recall_score(y_test, y_pred)), 4),
        "f1": round(float(f1_score(y_test, y_pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test))
    }

    # Persist model and metrics
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({
        "pipeline": pipeline,
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES
        },
        "target": TARGET
    }, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("Model saved to:", MODEL_PATH)
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()