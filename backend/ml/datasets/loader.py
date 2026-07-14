"""Dataset loading utilities for maternal health data.

This module handles loading datasets from disk with validation and
basic transformations. It acts as the single source of truth for
where and how to load training/validation/test data.

Design principles:
- Single responsibility: Just load data, don't engineer features
- Reproducibility: Document seed and split versions
- Validation: Basic checks that data is in expected format
"""

from pathlib import Path
from typing import Optional

import pandas as pd

# Default paths
BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
SYNTHETIC_DATA_PATH = BACKEND_ROOT / "ml" / "data" / "synthetic" / "pregnancy_risk_v1.csv"


def load_dataset(
    path: Optional[Path | str] = None,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Load a maternal health dataset from disk.

    Args:
        path: Path to CSV file. If None, uses default synthetic dataset.
        validate: Whether to run basic validation on loaded data.

    Returns:
        DataFrame with raw maternal health data.

    Raises:
        FileNotFoundError: If path doesn't exist.
        ValueError: If validation fails.

    Example:
        >>> df = load_dataset()
        >>> df.shape
        (5000, 37)
    """
    if path is None:
        path = SYNTHETIC_DATA_PATH

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)

    if validate:
        _validate_dataset(df)

    return df


def load_synthetic_dataset(validate: bool = True) -> pd.DataFrame:
    """
    Load the default synthetic maternal health dataset.

    This is the main dataset used for model training. It contains
    5,000 synthetically generated maternal health records with
    balanced risk distribution.

    Returns:
        DataFrame with 5,000 rows × 37 columns.

    Example:
        >>> df = load_synthetic_dataset()
        >>> df["risk_level"].value_counts()
        Low         2000
        Moderate    1500
        High        1000
        Emergency    500
    """
    return load_dataset(path=SYNTHETIC_DATA_PATH, validate=validate)


def _validate_dataset(df: pd.DataFrame) -> None:
    """
    Perform basic validation on loaded dataset.

    Checks:
    - No missing values
    - Expected columns present
    - Value ranges are realistic
    - No duplicate rows

    Args:
        df: DataFrame to validate.

    Raises:
        ValueError: If validation fails.
    """
    if df.empty:
        raise ValueError("Dataset is empty")

    if df.isna().any().any():
        raise ValueError("Dataset contains missing values")

    # Expected columns in synthetic data
    expected_cols = {
        "age",
        "height_cm",
        "weight_kg",
        "bmi",
        "weeks_pregnant",
        "systolic_bp",
        "diastolic_bp",
        "heart_rate",
        "body_temperature",
        "blood_sugar",
        "oxygen_saturation",
        "hemoglobin",
        "risk_level",
    }

    if not expected_cols.issubset(set(df.columns)):
        missing = expected_cols - set(df.columns)
        raise ValueError(f"Missing expected columns: {missing}")

    # Basic range validation
    if not (15 <= df["age"].min() <= 49):
        raise ValueError(f"Age range unrealistic: {df['age'].min()}-{df['age'].max()}")

    if (df["bmi"] < 12).any() or (df["bmi"] > 60).any():
        raise ValueError(f"BMI values unrealistic: {df['bmi'].min()}-{df['bmi'].max()}")

    if df.duplicated().any():
        raise ValueError(f"Dataset contains {df.duplicated().sum()} duplicate rows")
