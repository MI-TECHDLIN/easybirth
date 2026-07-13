from __future__ import annotations

from shared.features import feature_names, normalize_features
from shared.risk import risk_label
from shared.languages import is_supported_language


def test_feature_names_are_defined() -> None:
    assert feature_names() == ["age_weeks", "blood_pressure", "heart_rate", "weight_kg"]


def test_normalize_features_converts_to_float() -> None:
    assert normalize_features([1, 2, 3]) == [1.0, 2.0, 3.0]


def test_risk_label_mapping() -> None:
    assert risk_label(0.9) == "high"
    assert risk_label(0.5) == "medium"
    assert risk_label(0.1) == "low"


def test_supported_languages() -> None:
    assert is_supported_language("en") is True
    assert is_supported_language("fr") is False
