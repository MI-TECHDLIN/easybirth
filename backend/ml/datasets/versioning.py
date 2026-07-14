"""Dataset versioning utilities.

This module tracks dataset versions, checksums, and metadata to ensure
reproducibility and traceability throughout the ML pipeline.

Design:
- Each dataset snapshot gets a version
- Versions include checksum, sample count, split info
- Enables rollback and audit trails
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass
class DatasetVersion:
    """Metadata for a dataset version."""

    version: str  # e.g., "v1", "v1.1", "pregnancy_risk_v1"
    timestamp: str  # ISO format datetime
    rows: int  # Number of rows
    columns: int  # Number of columns
    checksum: str  # SHA256 of CSV file
    source: str  # "synthetic", "reference", etc.
    split_info: dict[str, int] | None = None  # {"train": 3500, "val": 750, "test": 750}
    description: str | None = None
    notes: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> DatasetVersion:
        """Create from dictionary."""
        return cls(**data)


def compute_checksum(df: pd.DataFrame | Path) -> str:
    """
    Compute SHA256 checksum of a dataset.

    Args:
        df: DataFrame or path to CSV file

    Returns:
        Hex digest of SHA256 hash
    """
    if isinstance(df, Path):
        # Hash file contents
        sha256 = hashlib.sha256()
        with open(df, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    else:
        # Hash DataFrame (sorted by columns for reproducibility)
        csv_str = df.sort_index(axis=1).to_csv(index=False)
        return hashlib.sha256(csv_str.encode()).hexdigest()


def create_version(
    df: pd.DataFrame | Path,
    version: str,
    source: str = "synthetic",
    description: str | None = None,
    split_info: dict[str, int] | None = None,
) -> DatasetVersion:
    """
    Create a new dataset version record.

    Args:
        df: Dataset (DataFrame or path to CSV)
        version: Version identifier (e.g., "v1", "pregnancy_risk_v1")
        source: Dataset source type
        description: Human-readable description
        split_info: Optional split information

    Returns:
        DatasetVersion with metadata

    Example:
        >>> df = pd.read_csv("pregnancy_risk_v1.csv")
        >>> version = create_version(
        ...     df,
        ...     version="v1",
        ...     description="Initial synthetic dataset",
        ...     split_info={"train": 3500, "val": 750, "test": 750}
        ... )
    """
    if isinstance(df, Path):
        df_to_check = pd.read_csv(df)
    else:
        df_to_check = df

    return DatasetVersion(
        version=version,
        timestamp=datetime.utcnow().isoformat(),
        rows=len(df_to_check),
        columns=len(df_to_check.columns),
        checksum=compute_checksum(df_to_check),
        source=source,
        split_info=split_info,
        description=description,
    )


def save_version_info(version: DatasetVersion, output_path: Path) -> None:
    """
    Save version metadata to JSON file.

    Args:
        version: DatasetVersion to save
        output_path: Path to write version_info.json
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(version.to_json())


def load_version_info(info_path: Path) -> DatasetVersion:
    """
    Load version metadata from JSON file.

    Args:
        info_path: Path to version_info.json

    Returns:
        Loaded DatasetVersion

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not info_path.exists():
        raise FileNotFoundError(f"Version info not found at {info_path}")

    with open(info_path) as f:
        data = json.load(f)

    return DatasetVersion.from_dict(data)
