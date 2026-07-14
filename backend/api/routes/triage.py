"""Triage router for the AI-powered voice risk assessment endpoint."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.triage import TriageRequest, TriageResponse
from api.services.triage_service import TriageService

router = APIRouter(prefix="/triage", tags=["triage"])
service = TriageService()


@router.post("", response_model=TriageResponse)
def assess_triage(payload: TriageRequest) -> TriageResponse:
    try:
        return service.assess(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
