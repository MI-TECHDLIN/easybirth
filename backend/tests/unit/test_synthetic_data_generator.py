from __future__ import annotations

from scripts.generate_synthetic_data import build_dataset, validate_dataset


def test_build_dataset_generates_expected_columns() -> None:
    df = build_dataset(samples=200, seed=7)

    assert not df.empty
    assert "risk_level" in df.columns
    assert {"Low", "Moderate", "High", "Emergency"}.issubset(set(df["risk_level"].unique()))


def test_validate_dataset_accepts_generated_rows() -> None:
    df = build_dataset(samples=200, seed=11)
    validate_dataset(df)
