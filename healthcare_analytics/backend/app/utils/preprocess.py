import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COL = "is_fraud"

NUMERIC_COLS = [
    "claim_amount", "patient_age", "days_in_hospital",
    "num_procedures", "prior_claims", "billing_code_count"
]

CATEGORICAL_COLS = [
    "provider_id", "procedure_code", "diagnosis_code", "is_in_network"
]

def load_data(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Optional cleanup
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()
    return df

def split_X_y(df: pd.DataFrame):
    if TARGET_COL not in df.columns:
        raise ValueError(f"Target column '{TARGET_COL}' not found in dataset.")
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL].astype(int)
    return X, y

def build_preprocess():
    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocess = ColumnTransformer(transformers=[
        ("num", numeric_pipe, NUMERIC_COLS),
        ("cat", categorical_pipe, CATEGORICAL_COLS),
    ])
    return preprocess