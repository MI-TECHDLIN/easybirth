"""Explainability routes for the API service."""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas.common import ExplanationResponse
from api.services.explainability_service import ExplainabilityService

router = APIRouter(prefix="/explanations", tags=["explainability"])
service = ExplainabilityService()


@router.get("", response_model=ExplanationResponse)
def get_explanation() -> ExplanationResponse:
    return service.explain()
