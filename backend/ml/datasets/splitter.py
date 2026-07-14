"""Dataset splitting utilities for reproducible train/val/test splits.

This module provides utilities for splitting datasets while maintaining:
- Stratification by target variable (risk_level)
- Reproducibility via fixed random seeds
- Type safety with clear contracts
- No data leakage between splits
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetSplit(NamedTuple):
    """Container for train/val/test split data."""

    train: pd.DataFrame
    val: pd.DataFrame
    test: pd.DataFrame

    @property
    def train_size(self) -> int:
        """Number of training samples."""
        return len(self.train)

    @property
    def val_size(self) -> int:
        """Number of validation samples."""
        return len(self.val)

    @property
    def test_size(self) -> int:
        """Number of test samples."""
        return len(self.test)

    @property
    def total_size(self) -> int:
        """Total number of samples."""
        return self.train_size + self.val_size + self.test_size

    def report(self) -> str:
        """Generate split report."""
        total = self.total_size
        train_pct = 100 * self.train_size / total
        val_pct = 100 * self.val_size / total
        test_pct = 100 * self.test_size / total

        return f"""Dataset Split Report
====================
Training:   {self.train_size:,} ({train_pct:.1f}%)
Validation: {self.val_size:,} ({val_pct:.1f}%)
Test:       {self.test_size:,} ({test_pct:.1f}%)
Total:      {total:,}
"""


def train_val_test_split(
    df: pd.DataFrame,
    train_size: float = 0.70,
    val_size: float = 0.15,
    test_size: float = 0.15,
    stratify_col: str = "risk_level",
    random_state: int = 42,
) -> DatasetSplit:
    """
    Split dataset into train/val/test with stratification.

    Ensures:
    - No overlap between splits
    - Risk distribution preserved in each split
    - Reproducible splits via fixed seed

    Args:
        df: Input DataFrame to split
        train_size: Fraction for training (0.0-1.0)
        val_size: Fraction for validation (0.0-1.0)
        test_size: Fraction for testing (0.0-1.0)
        stratify_col: Column to stratify by (usually "risk_level")
        random_state: Random seed for reproducibility

    Returns:
        DatasetSplit with train/val/test DataFrames

    Raises:
        ValueError: If sizes don't sum to 1.0 or invalid stratification

    Example:
        >>> from ml.datasets import train_val_test_split
        >>> df = pd.read_csv("synthetic_data.csv")
        >>> split = train_val_test_split(df)
        >>> split.train_size
        3500
        >>> split.report()
        Dataset Split Report
        ====================
        Training:   3500 (70.0%)
        Validation:  750 (15.0%)
        Test:        750 (15.0%)
        Total:      5000
    """
    # Validate size parameters
    total = train_size + val_size + test_size
    if not np.isclose(total, 1.0, atol=0.001):
        raise ValueError(f"Train/val/test sizes must sum to 1.0, got {total}")

    if train_size < 0 or val_size < 0 or test_size < 0:
        raise ValueError("All sizes must be non-negative")

    # Validate stratification column
    if stratify_col not in df.columns:
        raise ValueError(f"Stratification column '{stratify_col}' not in DataFrame")

    # Reset index for clean split
    df = df.reset_index(drop=True)

    # First split: train vs (val + test)
    temp_size = val_size + test_size  # Combined val+test fraction
    train, temp = train_test_split(
        df,
        test_size=temp_size,
        train_size=train_size,
        stratify=df[stratify_col],
        random_state=random_state,
    )

    # Second split: val vs test (within temp set)
    # Use different seed for second split to avoid overlap
    val_frac_of_temp = val_size / temp_size
    val, test = train_test_split(
        temp,
        test_size=1 - val_frac_of_temp,
        train_size=val_frac_of_temp,
        stratify=temp[stratify_col],
        random_state=random_state + 1,  # Different seed for second split
    )

    # Reset indices to 0-based for clean DataFrames
    train = train.reset_index(drop=True)
    val = val.reset_index(drop=True)
    test = test.reset_index(drop=True)

    return DatasetSplit(train=train, val=val, test=test)


class StratifiedTrainValTestSplit:
    """
    sklearn-compatible splitter for stratified train/val/test splits.

    This class wraps train_val_test_split() to provide an sklearn-like
    interface that can be used in pipelines.

    Example:
        >>> splitter = StratifiedTrainValTestSplit(random_state=42)
        >>> split = splitter.split(df)
        >>> split.train.shape
        (3500, 37)
    """

    def __init__(
        self,
        train_size: float = 0.70,
        val_size: float = 0.15,
        test_size: float = 0.15,
        stratify_col: str = "risk_level",
        random_state: int = 42,
    ):
        """
        Initialize the splitter.

        Args:
            train_size: Fraction for training
            val_size: Fraction for validation
            test_size: Fraction for testing
            stratify_col: Column to stratify by
            random_state: Random seed
        """
        self.train_size = train_size
        self.val_size = val_size
        self.test_size = test_size
        self.stratify_col = stratify_col
        self.random_state = random_state

    def split(self, df: pd.DataFrame) -> DatasetSplit:
        """
        Split dataset.

        Args:
            df: DataFrame to split

        Returns:
            DatasetSplit with train/val/test
        """
        return train_val_test_split(
            df,
            train_size=self.train_size,
            val_size=self.val_size,
            test_size=self.test_size,
            stratify_col=self.stratify_col,
            random_state=self.random_state,
        )
