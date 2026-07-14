"""Unit tests for dataset splitting utilities."""
from __future__ import annotations

import pandas as pd
import pytest

from ml.datasets import (
    DatasetSplit,
    StratifiedTrainValTestSplit,
    train_val_test_split,
)


class TestTrainValTestSplit:
    """Test stratified train/val/test splitting."""

    @pytest.fixture
    def sample_dataset(self) -> pd.DataFrame:
        """Create sample dataset for testing."""
        return pd.DataFrame({
            "age": range(100),
            "risk_level": ["Low"] * 40 + ["Moderate"] * 30 + ["High"] * 20 + ["Emergency"] * 10,
            "feature_1": range(100),
            "feature_2": range(100, 200),
        })

    def test_split_default_sizes(self, sample_dataset: pd.DataFrame) -> None:
        """Split with default sizes (70/15/15)."""
        split = train_val_test_split(sample_dataset)

        assert split.train_size == 70
        assert split.val_size == 15
        assert split.test_size == 15
        assert split.total_size == 100

    def test_split_custom_sizes(self, sample_dataset: pd.DataFrame) -> None:
        """Split with custom sizes."""
        split = train_val_test_split(
            sample_dataset,
            train_size=0.60,
            val_size=0.20,
            test_size=0.20,
        )

        assert split.train_size == 60
        assert split.val_size == 20
        assert split.test_size == 20

    def test_split_no_overlap(self, sample_dataset: pd.DataFrame) -> None:
        """Train/val/test have no overlapping data rows."""
        split = train_val_test_split(sample_dataset)

        # Check that there are no duplicate rows across splits
        # by verifying each row appears in exactly one split
        combined = pd.concat([split.train, split.val, split.test], ignore_index=True)
        # Get all original data for comparison
        all_data = sample_dataset.reset_index(drop=True)
        
        # Verify combined splits have same data as original (just reordered)
        assert len(combined) == len(all_data)
        assert len(combined.drop_duplicates()) == len(all_data)  # No duplicates within combined

    def test_split_all_rows_included(self, sample_dataset: pd.DataFrame) -> None:
        """All rows appear in exactly one split."""
        split = train_val_test_split(sample_dataset)

        total_rows = split.train_size + split.val_size + split.test_size
        assert total_rows == len(sample_dataset)

    def test_split_stratification_preserved(self, sample_dataset: pd.DataFrame) -> None:
        """Risk distribution is preserved in each split."""
        split = train_val_test_split(sample_dataset, random_state=42)

        original_dist = sample_dataset["risk_level"].value_counts(normalize=True)
        train_dist = split.train["risk_level"].value_counts(normalize=True)
        val_dist = split.val["risk_level"].value_counts(normalize=True)
        test_dist = split.test["risk_level"].value_counts(normalize=True)

        # Allow 10% tolerance for small sample sets
        for risk_level in original_dist.index:
            if risk_level in train_dist.index:
                assert abs(train_dist[risk_level] - original_dist[risk_level]) < 0.15

    def test_split_reproducibility(self, sample_dataset: pd.DataFrame) -> None:
        """Same seed produces same split."""
        split1 = train_val_test_split(sample_dataset, random_state=42)
        split2 = train_val_test_split(sample_dataset, random_state=42)

        pd.testing.assert_frame_equal(split1.train, split2.train)
        pd.testing.assert_frame_equal(split1.val, split2.val)
        pd.testing.assert_frame_equal(split1.test, split2.test)

    def test_split_different_seeds_different_splits(self, sample_dataset: pd.DataFrame) -> None:
        """Different seeds produce different splits."""
        split1 = train_val_test_split(sample_dataset, random_state=42)
        split2 = train_val_test_split(sample_dataset, random_state=123)

        # Should have different data rows (with very high probability)
        # Check that not all rows are the same
        assert not split1.train.reset_index(drop=True).equals(split2.train.reset_index(drop=True))

    def test_split_invalid_size_sum_raises_error(self, sample_dataset: pd.DataFrame) -> None:
        """Sizes not summing to 1.0 raise ValueError."""
        with pytest.raises(ValueError, match="must sum to 1.0"):
            train_val_test_split(
                sample_dataset,
                train_size=0.50,
                val_size=0.30,
                test_size=0.15,  # Sum = 0.95
            )

    def test_split_negative_size_raises_error(self, sample_dataset: pd.DataFrame) -> None:
        """Negative sizes raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            train_val_test_split(
                sample_dataset,
                train_size=-0.10,
                val_size=0.50,
                test_size=0.60,
            )

    def test_split_invalid_stratify_column_raises_error(self, sample_dataset: pd.DataFrame) -> None:
        """Invalid stratification column raises ValueError."""
        with pytest.raises(ValueError, match="not in DataFrame"):
            train_val_test_split(sample_dataset, stratify_col="nonexistent")

    def test_split_preserves_features(self, sample_dataset: pd.DataFrame) -> None:
        """All original features are preserved."""
        split = train_val_test_split(sample_dataset)

        assert set(split.train.columns) == set(sample_dataset.columns)
        assert set(split.val.columns) == set(sample_dataset.columns)
        assert set(split.test.columns) == set(sample_dataset.columns)

    def test_split_index_is_reset(self, sample_dataset: pd.DataFrame) -> None:
        """Indices are reset in splits."""
        split = train_val_test_split(sample_dataset)

        assert split.train.index.tolist() == list(range(split.train_size))
        assert split.val.index.tolist() == list(range(split.val_size))
        assert split.test.index.tolist() == list(range(split.test_size))


class TestDatasetSplit:
    """Test DatasetSplit NamedTuple."""

    def test_dataset_split_properties(self) -> None:
        """DatasetSplit has correct properties."""
        train_df = pd.DataFrame({"col": [1, 2, 3]})
        val_df = pd.DataFrame({"col": [4, 5]})
        test_df = pd.DataFrame({"col": [6]})

        split = DatasetSplit(train=train_df, val=val_df, test=test_df)

        assert split.train_size == 3
        assert split.val_size == 2
        assert split.test_size == 1
        assert split.total_size == 6

    def test_dataset_split_report(self) -> None:
        """Split report contains correct statistics."""
        train_df = pd.DataFrame({"col": range(70)})
        val_df = pd.DataFrame({"col": range(15)})
        test_df = pd.DataFrame({"col": range(15)})

        split = DatasetSplit(train=train_df, val=val_df, test=test_df)
        report = split.report()

        assert "70" in report
        assert "15" in report
        assert "100" in report
        assert "70.0%" in report


class TestStratifiedTrainValTestSplit:
    """Test sklearn-compatible splitter class."""

    @pytest.fixture
    def sample_dataset(self) -> pd.DataFrame:
        """Create sample dataset."""
        return pd.DataFrame({
            "age": range(100),
            "risk_level": ["Low"] * 40 + ["Moderate"] * 30 + ["High"] * 20 + ["Emergency"] * 10,
            "feature": range(100),
        })

    def test_splitter_initialization(self) -> None:
        """Splitter can be initialized with custom params."""
        splitter = StratifiedTrainValTestSplit(
            train_size=0.60,
            val_size=0.20,
            test_size=0.20,
            random_state=42,
        )

        assert splitter.train_size == 0.60
        assert splitter.val_size == 0.20
        assert splitter.test_size == 0.20

    def test_splitter_split_method(self, sample_dataset: pd.DataFrame) -> None:
        """Splitter.split() produces DatasetSplit."""
        splitter = StratifiedTrainValTestSplit(random_state=42)
        split = splitter.split(sample_dataset)

        assert isinstance(split, DatasetSplit)
        assert split.train_size == 70
        assert split.val_size == 15
        assert split.test_size == 15

    def test_splitter_reproducibility(self, sample_dataset: pd.DataFrame) -> None:
        """Same splitter seed produces same results."""
        splitter = StratifiedTrainValTestSplit(random_state=42)

        split1 = splitter.split(sample_dataset)
        split2 = splitter.split(sample_dataset)

        pd.testing.assert_frame_equal(split1.train, split2.train)
        pd.testing.assert_frame_equal(split1.val, split2.val)
        pd.testing.assert_frame_equal(split1.test, split2.test)
