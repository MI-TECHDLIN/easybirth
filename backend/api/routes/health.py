"""Health routes for the API service."""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
