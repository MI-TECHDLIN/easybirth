"""Shared feature helpers reused across API and ML layers."""
from __future__ import annotations

from typing import Iterable


def feature_names() -> list[str]:
    """Return the canonical set of feature names used by the project."""
    return ["age_weeks", "blood_pressure", "heart_rate", "weight_kg"]


def normalize_features(values: Iterable[float]) -> list[float]:
    """Normalize a sequence of numeric features to floats."""
    return [float(value) for value in values]
