# backend/ml_model/train_fraud.py
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier

# Paths
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "datasets" / "fraud_claims.csv"  # use your synthetic_health_claims.csv path if different
ML_DIR = ROOT / "backend" / "app" / "ml_models"
MODEL_PATH = ML_DIR / "fraud_model.pkl"
METRICS_PATH = ML_DIR / "fraud_metrics.json"
FEATURES_PATH = ML_DIR / "fraud_feature_names.json"

# Target inference: prefer 'is_fraud', else auto-detect a binary column
CANDIDATE_TARGETS = ["is_fraud", "fraud", "label"]

def infer_target_column(df: pd.DataFrame) -> str:
    for cand in CANDIDATE_TARGETS:
        if cand in df.columns:
            return cand
    # auto-detect: pick a column with {0,1} values if present
    for c in df.columns:
        vals = set(df[c].dropna().unique().tolist())
        if vals <= {0, 1}:
            return c
    raise ValueError("Target column not found. Expected one of is_fraud/fraud/label or a binary column.")

def infer_cols(X: pd.DataFrame):
    num = X.select_dtypes(include=[np.number]).columns.tolist()
    cat = X.select_dtypes(exclude=[np.number]).columns.tolist()
    return num, cat

def build_pipeline(num_cols: List[str], cat_cols: List[str]):
    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )
    clf = RandomForestClassifier(
        n_estimators=400,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )
    return Pipeline(steps=[("pre", pre), ("clf", clf)])

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset missing: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH).drop_duplicates()
    # Optional: drop clear leakage columns
    leakage_cols = [c for c in df.columns if any(k in c.lower() for k in ["outcome", "final", "adjudication"])]
    df = df.drop(columns=leakage_cols, errors="ignore")

    target = infer_target_column(df)
    X = df.drop(columns=[target])
    y = df[target].astype(int)

    num_cols, cat_cols = infer_cols(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipe = build_pipeline(num_cols, cat_cols)
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else None

    report = classification_report(y_test, y_pred, output_dict=True)
    roc = roc_auc_score(y_test, y_proba) if y_proba is not None else None

    metrics = {
        "accuracy": report["accuracy"],
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1": report["1"]["f1-score"],
        "roc_auc": roc
    }

    ML_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    feature_names = {
        "numeric": num_cols,
        "categorical": cat_cols,
        "all_features": num_cols + cat_cols,
        "target": target
    }
    with open(FEATURES_PATH, "w") as f:
        json.dump(feature_names, f, indent=2)

    print("Saved model:", MODEL_PATH)
    print("Saved metrics:", METRICS_PATH)
    print("Saved feature names:", FEATURES_PATH)
    print("Metrics:", json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()