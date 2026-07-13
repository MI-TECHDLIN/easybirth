"""Placeholder risk service."""
from __future__ import annotations

from api.schemas.risk import RiskAssessmentRequest, RiskAssessmentResponse


class RiskService:
    def predict(self, payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
        return RiskAssessmentResponse(
            risk_level="high",
            confidence=0.92,
            model_version="0.1.0-dev",
            message="Placeholder risk assessment",
        )
