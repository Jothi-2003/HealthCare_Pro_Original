import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def build_preprocessor(df: pd.DataFrame, target: str):
    """
    Build preprocessing: impute numeric/categorical, one-hot categorical.
    Dates and identifiers remain categorical (string) and will be one-hot encoded.
    """
    feature_df = df.drop(columns=[target], errors="ignore")

    # Booleans will be handled as categorical for one-hot; numeric excludes booleans
    bool_cols = feature_df.select_dtypes(include=["bool"]).columns.tolist()
    num_cols = feature_df.select_dtypes(include=["number"]).columns.difference(bool_cols).tolist()
    cat_cols = feature_df.select_dtypes(include=["object", "category"]).columns.tolist()
    cat_cols += bool_cols  # treat booleans as categorical

    numeric = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categorical, cat_cols),
        ],
        remainder="drop"
    )
    return preprocessor, num_cols, cat_cols