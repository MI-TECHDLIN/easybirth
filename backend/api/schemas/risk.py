"""Risk assessment schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RiskAssessmentRequest(BaseModel):
    age_weeks: int = Field(..., ge=0)
    blood_pressure: float = Field(..., ge=0)
    heart_rate: int = Field(..., ge=0)
    weight_kg: float = Field(..., ge=0)
    language: str = Field(default="en")


class RiskAssessmentResponse(BaseModel):
    risk_level: str = Field(default="high")
    confidence: float = Field(default=0.92)
    model_version: str = Field(default="0.1.0-dev")
    message: str = Field(default="Placeholder risk assessment")
