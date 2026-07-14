import joblib
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from ml.datasets import load_synthetic_dataset, train_val_test_split
from ml.feature_engineering.feature_pipeline import engineer_features


def _map_target_to_binary(df: pd.DataFrame) -> pd.DataFrame:
    # Map risk_level to binary emergency (Emergency vs not)
    df = df.copy()
    df["target"] = (df["risk_level"] == "Emergency").astype(int)
    return df


def test_end_to_end_save_load_model(tmp_path: Path) -> None:
    """End-to-end pipeline: load -> split -> features -> train -> save/load -> predict"""
    df = load_synthetic_dataset()
    df = _map_target_to_binary(df)

    split = train_val_test_split(df, random_state=42)
    # Ensure no duplicated rows across concatenated splits
    combined = pd.concat([split.train, split.val, split.test], ignore_index=True)
    assert combined.drop_duplicates().shape[0] == combined.shape[0]

    # Engineer features for training and testing (use a subset to keep runtime small)
    X_train = pd.concat([engineer_features(r.to_dict()) for _, r in split.train.iterrows()], ignore_index=True)
    X_test = pd.concat([engineer_features(r.to_dict()) for _, r in split.test.iterrows()], ignore_index=True)

    y_train = split.train["target"].reset_index(drop=True)
    y_test = split.test["target"].reset_index(drop=True)

    # Train a small deterministic model
    model = LogisticRegression(solver="liblinear", random_state=42, max_iter=200)
    model.fit(X_train.select_dtypes(include=["number"]), y_train)

    preds_before = model.predict(X_test.select_dtypes(include=["number"]))

    # Save and reload
    model_path = tmp_path / "model.joblib"
    joblib.dump(model, model_path)
    loaded = joblib.load(model_path)

    preds_after = loaded.predict(X_test.select_dtypes(include=["number"]))

    assert (preds_before == preds_after).all()


def test_no_target_leakage_in_features() -> None:
    """Engineered features should not include the target column or leak the label."""
    df = load_synthetic_dataset()
    sample_records = df.sample(10, random_state=1)
    engineered = pd.concat(
        [engineer_features(row.to_dict()) for _, row in sample_records.iterrows()],
        ignore_index=True,
    )

    # Target column must not be present
    assert "risk_level" not in engineered.columns
    assert "target" not in engineered.columns

    # No feature column should match the label across all sampled rows.
    # This is a soft heuristic for direct leakage rather than exact value matching
    # on a single random example.
    target_values = (sample_records["risk_level"] == "Emergency").astype(int)
    numeric_cols = engineered.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        if engineered[col].nunique() == 1:
            # If the feature is constant, it is not a direct indicator of the
            # sampled risk label values across the sample.
            continue
        assert not (engineered[col].to_numpy() == target_values.to_numpy()).all()


def test_reproducible_model_training_seeded() -> None:
    """Training with the same random_state should produce identical coefficients."""
    df = load_synthetic_dataset()
    df = _map_target_to_binary(df)
    split = train_val_test_split(df, random_state=123)

    X_train = pd.concat([engineer_features(r.to_dict()) for _, r in split.train.iterrows()], ignore_index=True)
    y_train = split.train["target"].reset_index(drop=True)

    X = X_train.select_dtypes(include=["number"]).values
    y = y_train.values

    m1 = LogisticRegression(solver="liblinear", random_state=42, max_iter=200)
    m2 = LogisticRegression(solver="liblinear", random_state=42, max_iter=200)
    m1.fit(X, y)
    m2.fit(X, y)

    assert np.allclose(m1.coef_, m2.coef_)
