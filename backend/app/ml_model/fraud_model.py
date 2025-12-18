# backend/train_fraud_model.py
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import Pipeline
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.utils.preprocess import build_preprocessor

logger = configure_logging()

# 1) Load dataset
csv_path = Path("datasets/synthetic_health_claims.csv")
df = pd.read_csv(csv_path)

# 2) Define target column (override with env if different)
target = settings.TARGET_COLUMN
if target not in df.columns:
    raise ValueError(f"Target column '{target}' not found. Please set FRAUD_TARGET_COLUMN env or rename in CSV.")

# 3) Split features/target
y = df[target].astype(int)  # ensure binary 0/1
X = df.drop(columns=[target])

# Optional: remove pure identifiers that should not be used as features
for col in ["claim_id"]:
    if col in X.columns:
        X = X.drop(columns=[col])

# 4) Build preprocessing
preprocessor, num_cols, cat_cols = build_preprocessor(pd.concat([X, y], axis=1), target)
logger.info(f"Numeric cols: {num_cols}")
logger.info(f"Categorical cols: {cat_cols}")

# 5) Define model
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

# 6) Pipeline = preprocessor + classifier
clf = Pipeline(steps=[("pre", preprocessor), ("rf", rf)])

# 7) Train/val split
from sklearn.model_selection import train_test_split
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

# 11) Optionally save metrics sidecar
metrics = {"accuracy": float(acc), "auc": float(auc) if auc is not None else None}
joblib.dump(metrics, model_path.with_suffix(".metrics.pkl"))
logger.info(f"Saved metrics to {model_path.with_suffix('.metrics.pkl').resolve()}")