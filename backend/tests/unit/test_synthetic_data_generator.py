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


def test_build_dataset_generates_valid_bp_pairs() -> None:
    df = build_dataset(samples=200, seed=13)
    assert (df["systolic_bp"] > df["diastolic_bp"]).all()


def test_validate_dataset_rejects_invalid_bp_pairs() -> None:
    df = build_dataset(samples=10, seed=17)
    df.loc[0, "systolic_bp"] = df.loc[0, "diastolic_bp"]
    try:
        validate_dataset(df)
        raise AssertionError("Expected validate_dataset to fail on invalid BP pair")
    except ValueError as exc:
        assert "Systolic BP must be greater than diastolic BP" in str(exc)
