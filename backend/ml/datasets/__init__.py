"""Dataset handling module for maternal health ML pipeline.

This module provides utilities for loading, splitting, and versioning datasets
while maintaining clean separation of concerns:

- loader.py: Load raw datasets from disk
- splitter.py: Split data into train/val/test with reproducibility
- versioning.py: Track dataset versions and checksums

Design principle: Single responsibility pattern allows training code to focus
on ML logic without worrying about data loading/splitting details.

Example:
    >>> from ml.datasets import load_synthetic_dataset, train_val_test_split
    >>> df = load_synthetic_dataset()
    >>> split = train_val_test_split(df)
    >>> X_train = split.train.drop("risk_level", axis=1)
    >>> y_train = split.train["risk_level"]
"""

from .loader import load_dataset, load_synthetic_dataset
from .splitter import DatasetSplit, StratifiedTrainValTestSplit, train_val_test_split
from .versioning import DatasetVersion, compute_checksum, create_version, load_version_info, save_version_info

__all__ = [
    # Loading
    "load_dataset",
    "load_synthetic_dataset",
    # Splitting
    "train_val_test_split",
    "StratifiedTrainValTestSplit",
    "DatasetSplit",
    # Versioning
    "DatasetVersion",
    "compute_checksum",
    "create_version",
    "save_version_info",
    "load_version_info",
]
