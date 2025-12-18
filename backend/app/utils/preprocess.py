import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def build_preprocessor(df: pd.DataFrame, target: str):
    # Infer feature types
    feature_df = df.drop(columns=[target], errors="ignore")
    cat_cols = feature_df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = feature_df.select_dtypes(include=["number", "bool"]).columns.tolist()

    numeric = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])
    categorical = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categorical, cat_cols),
        ],
        remainder="drop"
    )
    return preprocessor, num_cols, cat_cols