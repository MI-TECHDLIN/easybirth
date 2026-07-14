"""Unit tests for dataset loading utilities."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

from ml.datasets import load_dataset, load_synthetic_dataset


class TestLoadDataset:
    """Test generic dataset loading."""

    def test_load_default_synthetic_dataset(self) -> None:
        """Load default synthetic dataset."""
        df = load_dataset()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5000
        assert df.shape[1] == 37

    def test_load_synthetic_dataset_has_required_columns(self) -> None:
        """Verify required columns are present."""
        df = load_dataset()
        required = {"age", "risk_level", "bmi", "systolic_bp", "diastolic_bp"}
        assert required.issubset(set(df.columns))

    def test_load_dataset_from_custom_path(self) -> None:
        """Load dataset from custom path."""
        with TemporaryDirectory() as tmpdir:
            # Create test CSV
            test_df = pd.DataFrame({
                "age": [25, 30, 35],
                "risk_level": ["Low", "Moderate", "High"],
                "bmi": [22.0, 24.5, 26.0],
                "systolic_bp": [110, 120, 130],
                "diastolic_bp": [70, 80, 90],
            })
            test_path = Path(tmpdir) / "test_data.csv"
            test_df.to_csv(test_path, index=False)

            # Load and verify
            df = load_dataset(path=test_path, validate=False)
            assert len(df) == 3
            assert df["age"].tolist() == [25, 30, 35]

    def test_load_nonexistent_file_raises_error(self) -> None:
        """Raise error when file not found."""
        with pytest.raises(FileNotFoundError):
            load_dataset(path="/nonexistent/path/data.csv")

    def test_load_dataset_without_validation(self) -> None:
        """Load dataset without validation (skip checks)."""
        df = load_dataset(validate=False)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5000

    def test_load_dataset_with_validation_passes(self) -> None:
        """Load with validation passes for synthetic data."""
        df = load_dataset(validate=True)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5000

    def test_load_resets_index(self) -> None:
        """Index is reset after loading."""
        df = load_dataset()
        assert df.index.tolist() == list(range(len(df)))


class TestLoadSyntheticDataset:
    """Test synthetic dataset loading."""

    def test_load_synthetic_dataset_default(self) -> None:
        """Load default synthetic dataset."""
        df = load_synthetic_dataset()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5000
        assert df.shape[1] == 37

    def test_synthetic_dataset_no_missing_values(self) -> None:
        """Synthetic dataset has no missing values."""
        df = load_synthetic_dataset()
        assert not df.isna().any().any()

    def test_synthetic_dataset_risk_distribution(self) -> None:
        """Risk distribution is as expected (40/30/20/10)."""
        df = load_synthetic_dataset()
        counts = df["risk_level"].value_counts(normalize=True).sort_index()

        # Allow 5% tolerance
        assert 0.35 < counts.get("Low", 0) < 0.45
        assert 0.25 < counts.get("Moderate", 0) < 0.35
        assert 0.15 < counts.get("High", 0) < 0.25
        assert 0.05 < counts.get("Emergency", 0) < 0.15

    def test_synthetic_dataset_age_range(self) -> None:
        """Age values are within realistic range [15-49]."""
        df = load_synthetic_dataset()
        assert 15 <= df["age"].min()
        assert df["age"].max() <= 49

    def test_synthetic_dataset_pregnancy_weeks(self) -> None:
        """Pregnancy weeks are within range [1-42]."""
        df = load_synthetic_dataset()
        assert 1 <= df["weeks_pregnant"].min()
        assert df["weeks_pregnant"].max() <= 42

    def test_synthetic_dataset_bmi_range(self) -> None:
        """BMI is within realistic range [12-60]."""
        df = load_synthetic_dataset()
        assert 12 <= df["bmi"].min()
        assert df["bmi"].max() <= 60

    def test_synthetic_dataset_blood_pressure_ranges(self) -> None:
        """Blood pressure values are realistic."""
        df = load_synthetic_dataset()
        # Systolic: 60-220, Diastolic: 40-140
        assert 60 <= df["systolic_bp"].min()
        assert df["systolic_bp"].max() <= 220
        assert 40 <= df["diastolic_bp"].min()
        assert df["diastolic_bp"].max() <= 140

    def test_synthetic_dataset_no_duplicates(self) -> None:
        """Synthetic dataset has no duplicate rows."""
        df = load_synthetic_dataset()
        assert not df.duplicated().any()

    def test_synthetic_dataset_reproducibility(self) -> None:
        """Loading twice produces identical data."""
        df1 = load_synthetic_dataset()
        df2 = load_synthetic_dataset()
        pd.testing.assert_frame_equal(df1, df2)


class TestDatasetValidation:
    """Test dataset validation logic."""

    def test_validate_empty_dataset_raises_error(self) -> None:
        """Empty dataset raises ValueError."""
        from ml.datasets.loader import _validate_dataset

        df = pd.DataFrame()
        with pytest.raises(ValueError, match="Dataset is empty"):
            _validate_dataset(df)

    def test_validate_missing_values_raises_error(self) -> None:
        """Dataset with missing values raises ValueError."""
        from ml.datasets.loader import _validate_dataset

        df = pd.DataFrame({
            "age": [25, None, 35],
            "risk_level": ["Low", "Moderate", "High"],
        })
        with pytest.raises(ValueError, match="missing values"):
            _validate_dataset(df)

    def test_validate_missing_expected_columns(self) -> None:
        """Missing expected columns raises ValueError."""
        from ml.datasets.loader import _validate_dataset

        df = pd.DataFrame({"some_col": [1, 2, 3]})
        with pytest.raises(ValueError, match="Missing expected columns"):
            _validate_dataset(df)

    def test_validate_unrealistic_age_range(self) -> None:
        """Unrealistic age range raises ValueError."""
        from ml.datasets.loader import _validate_dataset

        df = pd.DataFrame({
            "age": [5, 10, 12],  # Too young
            "height_cm": [150, 160, 170],
            "weight_kg": [50, 60, 70],
            "bmi": [22.0, 23.5, 24.0],
            "weeks_pregnant": [20, 25, 30],
            "systolic_bp": [110, 120, 130],
            "diastolic_bp": [70, 80, 90],
            "heart_rate": [80, 85, 90],
            "body_temperature": [36.5, 36.6, 36.7],
            "blood_sugar": [90, 95, 100],
            "oxygen_saturation": [97.0, 97.5, 98.0],
            "hemoglobin": [12.0, 12.5, 13.0],
            "risk_level": ["Low", "Moderate", "High"],
        })
        with pytest.raises(ValueError, match="Age range unrealistic"):
            _validate_dataset(df)

    def test_validate_unrealistic_bmi(self) -> None:
        """BMI outside range raises ValueError."""
        from ml.datasets.loader import _validate_dataset

        df = pd.DataFrame({
            "age": [25, 30, 35],
            "height_cm": [150, 160, 170],
            "weight_kg": [50, 60, 70],
            "bmi": [5.0, 23.5, 80.0],  # First and last are unrealistic
            "weeks_pregnant": [20, 25, 30],
            "systolic_bp": [110, 120, 130],
            "diastolic_bp": [70, 80, 90],
            "heart_rate": [80, 85, 90],
            "body_temperature": [36.5, 36.6, 36.7],
            "blood_sugar": [90, 95, 100],
            "oxygen_saturation": [97.0, 97.5, 98.0],
            "hemoglobin": [12.0, 12.5, 13.0],
            "risk_level": ["Low", "Moderate", "High"],
        })
        with pytest.raises(ValueError, match="BMI values unrealistic"):
            _validate_dataset(df)
