"""Placeholder explainability service."""
from __future__ import annotations

from api.schemas.common import ExplanationResponse


class ExplainabilityService:
    def explain(self) -> ExplanationResponse:
        return ExplanationResponse(
            explanation="Placeholder explanation",
            model_version="0.1.0-dev",
        )
