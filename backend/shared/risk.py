"""Shared risk-related helpers used by multiple application layers."""
from __future__ import annotations


def risk_label(score: float) -> str:
    """Convert a numeric risk score into a simple label."""
    if score >= 0.75:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"
