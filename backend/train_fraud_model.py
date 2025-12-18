import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.utils.preprocess import build_preprocessor

logger = configure_logging()

IDENTIFIER_COLS = [
    "Claim_ID", "Patient_ID", "Policy_Number", "Hospital_ID"
]

def main():
    # 1) Load dataset
    csv_path = Path("datasets/synthetic_health_claims.csv")
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {csv_path.resolve()}")
    df = pd.read_csv(csv_path)

    # 2) Target column
    target = settings.TARGET_COLUMN
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset")

    # 3) Split features/target
    y = df[target].astype(int)
    X = df.drop(columns=[target])

    # Drop identifiers (not predictive, can leak information)
    for col in IDENTIFIER_COLS:
        if col in X.columns:
            X = X.drop(columns=[col])

    # 4) Preprocessor
    preprocessor, num_cols, cat_cols = build_preprocessor(df, target)
    logger.info(f"Numeric cols: {num_cols}")
    logger.info(f"Categorical cols: {cat_cols}")

    # 5) Model
    rf = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    # 6) Pipeline
    clf = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", rf)])

    # 7) Train/val split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 8) Fit
    clf.fit(X_train, y_train)

    # 9) Evaluate
    y_pred = clf.predict(X_test)
    y_proba = clf.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, y_pred)
    try:
        auc = roc_auc_score(y_test, y_proba)
    except Exception:
        auc = None

    logger.info(f"Accuracy: {acc:.4f} | AUC: {auc if auc is not None else 'NA'}")

    # 10) Save model
    model_path = Path(settings.MODEL_PATH)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, model_path)
    logger.info(f"Saved model to {model_path.resolve()}")

    # 11) Save metrics
    metrics = {"accuracy": float(acc), "auc": float(auc) if auc is not None else None}
    joblib.dump(metrics, model_path.with_suffix(".metrics.pkl"))
    logger.info(f"Saved metrics to {model_path.with_suffix('.metrics.pkl').resolve()}")

    print("✅ Model trained and saved successfully!")

if __name__ == "__main__":
    main()