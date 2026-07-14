"""Minimal training pipeline for integration and reproducibility tests.

This pipeline is intentionally small: it loads data, splits, engineers
features, scales numeric columns (fit on train only), trains a simple
logistic regression, saves the model and scaler, and returns artifacts.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from ml.datasets import load_dataset, train_val_test_split
from ml.feature_engineering.feature_pipeline import engineer_features


def run_training(
    data_path: Path | None = None,
    output_dir: Path | None = None,
    random_state: int = 42,
    numeric_features: list[str] | None = None,
) -> Dict[str, Any]:
    """Run a minimal training workflow and return artifacts.

    Args:
        data_path: Optional path to CSV dataset. If None, uses default synthetic.
        output_dir: Directory to save model artifacts. If None, artifacts are not saved.
        random_state: Seed for reproducibility.
        numeric_features: numeric columns to scale and use for training.

    Returns:
        Dict containing model, scaler, splits, and predictions on test set.
    """
    # Load dataset
    df = load_dataset(path=data_path, validate=True)

    # Split
    split = train_val_test_split(df, random_state=random_state)

    # Engineer features for each split
    def eng(df_in: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in df_in.iterrows():
            results.append(engineer_features(row.to_dict()))
        return pd.concat(results, ignore_index=True)

    X_train = eng(split.train)
    X_val = eng(split.val)
    X_test = eng(split.test)

    # Default numeric features if not provided
    if numeric_features is None:
        numeric_features = ["bmi", "map", "pulse_pressure", "age", "weeks_pregnant"]

    # Fit scaler on training numeric features only
    scaler = StandardScaler()
    scaler.fit(X_train[numeric_features])

    X_train_scaled = scaler.transform(X_train[numeric_features])
    X_val_scaled = scaler.transform(X_val[numeric_features])
    X_test_scaled = scaler.transform(X_test[numeric_features])

    # Use risk_level as target (map to binary: Emergency vs others)
    y_train = (split.train["risk_level"] == "Emergency").astype(int)
    y_val = (split.val["risk_level"] == "Emergency").astype(int)
    y_test = (split.test["risk_level"] == "Emergency").astype(int)

    # Train simple logistic regression
    model = LogisticRegression(random_state=random_state, max_iter=200)
    model.fit(X_train_scaled, y_train)

    # Predictions
    preds_test = model.predict(X_test_scaled)
    probs_test = model.predict_proba(X_test_scaled)[:, 1]

    artifacts: Dict[str, Any] = {
        "model": model,
        "scaler": scaler,
        "split": split,
        "X_train": X_train,
        "X_val": X_val,
        "X_test": X_test,
        "y_test": y_test,
        "preds_test": preds_test,
        "probs_test": probs_test,
    }

    # Save artifacts if requested
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, output_dir / "model.joblib")
        joblib.dump(scaler, output_dir / "scaler.joblib")

    return artifacts
