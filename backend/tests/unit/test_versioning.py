"""Unit tests for dataset versioning utilities."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from ml.datasets import (
    DatasetVersion,
    compute_checksum,
    create_version,
    load_version_info,
    save_version_info,
)


class TestComputeChecksum:
    """Test checksum computation."""

    def test_compute_checksum_from_dataframe(self) -> None:
        """Compute checksum from DataFrame."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        checksum = compute_checksum(df)

        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA256 hex digest is 64 chars

    def test_checksum_deterministic(self) -> None:
        """Same DataFrame always produces same checksum."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

        checksum1 = compute_checksum(df)
        checksum2 = compute_checksum(df)

        assert checksum1 == checksum2

    def test_checksum_different_for_different_data(self) -> None:
        """Different DataFrames produce different checksums."""
        df1 = pd.DataFrame({"col1": [1, 2, 3]})
        df2 = pd.DataFrame({"col1": [1, 2, 4]})

        checksum1 = compute_checksum(df1)
        checksum2 = compute_checksum(df2)

        assert checksum1 != checksum2

    def test_compute_checksum_from_csv_file(self) -> None:
        """Compute checksum from CSV file."""
        with TemporaryDirectory() as tmpdir:
            # Create test CSV
            df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
            csv_path = Path(tmpdir) / "test.csv"
            df.to_csv(csv_path, index=False)

            checksum = compute_checksum(csv_path)

            assert isinstance(checksum, str)
            assert len(checksum) == 64

    def test_checksum_file_deterministic(self) -> None:
        """Checksum for same file is always the same."""
        with TemporaryDirectory() as tmpdir:
            df = pd.DataFrame({"col1": [1, 2, 3]})
            csv_path = Path(tmpdir) / "test.csv"
            df.to_csv(csv_path, index=False)

            checksum1 = compute_checksum(csv_path)
            checksum2 = compute_checksum(csv_path)

            assert checksum1 == checksum2


class TestDatasetVersion:
    """Test DatasetVersion dataclass."""

    def test_version_creation(self) -> None:
        """Create DatasetVersion."""
        version = DatasetVersion(
            version="v1",
            timestamp="2024-01-01T00:00:00",
            rows=100,
            columns=10,
            checksum="abc123",
            source="synthetic",
        )

        assert version.version == "v1"
        assert version.rows == 100
        assert version.columns == 10

    def test_version_to_dict(self) -> None:
        """Convert version to dictionary."""
        version = DatasetVersion(
            version="v1",
            timestamp="2024-01-01T00:00:00",
            rows=100,
            columns=10,
            checksum="abc123",
            source="synthetic",
        )

        data = version.to_dict()

        assert data["version"] == "v1"
        assert data["rows"] == 100
        assert isinstance(data, dict)

    def test_version_to_json(self) -> None:
        """Convert version to JSON."""
        version = DatasetVersion(
            version="v1",
            timestamp="2024-01-01T00:00:00",
            rows=100,
            columns=10,
            checksum="abc123",
            source="synthetic",
        )

        json_str = version.to_json()

        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["version"] == "v1"

    def test_version_from_dict(self) -> None:
        """Create version from dictionary."""
        data = {
            "version": "v1",
            "timestamp": "2024-01-01T00:00:00",
            "rows": 100,
            "columns": 10,
            "checksum": "abc123",
            "source": "synthetic",
            "split_info": None,
            "description": None,
            "notes": None,
        }

        version = DatasetVersion.from_dict(data)

        assert version.version == "v1"
        assert version.rows == 100

    def test_version_with_split_info(self) -> None:
        """Version can include split information."""
        split_info = {"train": 700, "val": 150, "test": 150}
        version = DatasetVersion(
            version="v1",
            timestamp="2024-01-01T00:00:00",
            rows=1000,
            columns=10,
            checksum="abc123",
            source="synthetic",
            split_info=split_info,
        )

        assert version.split_info == split_info

    def test_version_with_description(self) -> None:
        """Version can include description."""
        version = DatasetVersion(
            version="v1",
            timestamp="2024-01-01T00:00:00",
            rows=100,
            columns=10,
            checksum="abc123",
            source="synthetic",
            description="Initial synthetic dataset",
        )

        assert version.description == "Initial synthetic dataset"


class TestCreateVersion:
    """Test version creation."""

    def test_create_version_from_dataframe(self) -> None:
        """Create version from DataFrame."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

        version = create_version(df, version="v1", source="synthetic")

        assert version.version == "v1"
        assert version.source == "synthetic"
        assert version.rows == 3
        assert version.columns == 2
        assert len(version.checksum) == 64

    def test_create_version_from_file(self) -> None:
        """Create version from CSV file."""
        with TemporaryDirectory() as tmpdir:
            df = pd.DataFrame({"col1": [1, 2, 3]})
            csv_path = Path(tmpdir) / "test.csv"
            df.to_csv(csv_path, index=False)

            version = create_version(csv_path, version="v1")

            assert version.rows == 3
            assert version.columns == 1

    def test_create_version_with_description(self) -> None:
        """Create version with description."""
        df = pd.DataFrame({"col": [1, 2, 3]})

        version = create_version(
            df,
            version="v1",
            description="Test dataset",
        )

        assert version.description == "Test dataset"

    def test_create_version_with_split_info(self) -> None:
        """Create version with split information."""
        df = pd.DataFrame({"col": [1, 2, 3]})
        split_info = {"train": 2, "val": 1, "test": 0}

        version = create_version(df, version="v1", split_info=split_info)

        assert version.split_info == split_info

    def test_create_version_timestamp_populated(self) -> None:
        """Created version has timestamp."""
        df = pd.DataFrame({"col": [1, 2, 3]})

        version = create_version(df, version="v1")

        assert version.timestamp is not None
        assert "T" in version.timestamp  # ISO format


class TestSaveLoadVersion:
    """Test saving and loading versions."""

    def test_save_version_info(self) -> None:
        """Save version info to JSON file."""
        with TemporaryDirectory() as tmpdir:
            version = DatasetVersion(
                version="v1",
                timestamp="2024-01-01T00:00:00",
                rows=100,
                columns=10,
                checksum="abc123",
                source="synthetic",
            )

            output_path = Path(tmpdir) / "version_info.json"
            save_version_info(version, output_path)

            assert output_path.exists()

    def test_save_creates_directory(self) -> None:
        """Save creates parent directories if needed."""
        with TemporaryDirectory() as tmpdir:
            version = DatasetVersion(
                version="v1",
                timestamp="2024-01-01T00:00:00",
                rows=100,
                columns=10,
                checksum="abc123",
                source="synthetic",
            )

            output_path = Path(tmpdir) / "subdir" / "version_info.json"
            save_version_info(version, output_path)

            assert output_path.exists()

    def test_load_version_info(self) -> None:
        """Load version info from JSON file."""
        with TemporaryDirectory() as tmpdir:
            # Create and save version
            original = DatasetVersion(
                version="v1",
                timestamp="2024-01-01T00:00:00",
                rows=100,
                columns=10,
                checksum="abc123",
                source="synthetic",
            )

            output_path = Path(tmpdir) / "version_info.json"
            save_version_info(original, output_path)

            # Load and verify
            loaded = load_version_info(output_path)

            assert loaded.version == original.version
            assert loaded.rows == original.rows
            assert loaded.checksum == original.checksum

    def test_load_nonexistent_file_raises_error(self) -> None:
        """Loading nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_version_info(Path("/nonexistent/version_info.json"))

    def test_roundtrip_version(self) -> None:
        """Save and load produces identical version."""
        with TemporaryDirectory() as tmpdir:
            original = DatasetVersion(
                version="v1",
                timestamp="2024-01-01T12:34:56",
                rows=5000,
                columns=37,
                checksum="abc123def456",
                source="synthetic",
                split_info={"train": 3500, "val": 750, "test": 750},
                description="Initial pregnancy dataset",
            )

            output_path = Path(tmpdir) / "version_info.json"
            save_version_info(original, output_path)
            loaded = load_version_info(output_path)

            assert loaded.version == original.version
            assert loaded.timestamp == original.timestamp
            assert loaded.rows == original.rows
            assert loaded.columns == original.columns
            assert loaded.checksum == original.checksum
            assert loaded.source == original.source
            assert loaded.split_info == original.split_info
            assert loaded.description == original.description
