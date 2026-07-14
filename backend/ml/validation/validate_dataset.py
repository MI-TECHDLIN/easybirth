"""Validate generated synthetic data before training."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_dataset(path: str | Path) -> None:
    df = pd.read_csv(path)
    if df.isna().any().any():
        raise ValueError("Dataset contains missing values")
    if df.empty:
        raise ValueError("Dataset is empty")
    if not (15 <= df["age"].min() <= 49):
        raise ValueError("Age range is unrealistic")
    if not (1 <= df["weeks_pregnant"].min() <= 42):
        raise ValueError("Pregnancy week range is unrealistic")
    if (df["bmi"] < 12).any() or (df["bmi"] > 60).any():
        raise ValueError("BMI values are unrealistic")
    if (df["systolic_bp"] < 60).any() or (df["systolic_bp"] > 220).any():
        raise ValueError("Systolic BP values are unrealistic")
    if (df["diastolic_bp"] < 40).any() or (df["diastolic_bp"] > 140).any():
        raise ValueError("Diastolic BP values are unrealistic")
    if (df["systolic_bp"] <= df["diastolic_bp"]).any():
        raise ValueError("Systolic BP must be greater than diastolic BP for all rows")
    if df.duplicated().any():
        raise ValueError("Dataset contains duplicate rows")
    print("Dataset validation passed")


if __name__ == "__main__":
    validate_dataset("backend/ml/data/synthetic/pregnancy_risk_v1.csv")
