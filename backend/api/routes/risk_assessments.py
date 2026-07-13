"""Risk assessment routes for the API service."""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas.risk import RiskAssessmentRequest, RiskAssessmentResponse
from api.services.risk_service import RiskService

router = APIRouter(prefix="/risk-assessments", tags=["risk"])
service = RiskService()


@router.post("", response_model=RiskAssessmentResponse)
def create_risk_assessment(payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
    return service.predict(payload)
