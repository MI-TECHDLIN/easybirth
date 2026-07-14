"""Triage request and response schemas for AI risk assessment."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class ConversationTurn(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(...)


class TriageRequest(BaseModel):
    transcript: str = Field(..., description="Raw speech text from Flutter")
    language: str = Field(..., description="Target language code, e.g. 'hausa'")
    session_id: str = Field(..., description="UUID for the triage session")
    conversation_history: List[ConversationTurn] = Field(default_factory=list)
    gestational_week: int = Field(..., ge=0)
    patient_name: str = Field(default="Patient")
    chw_phone: str | None = Field(default=None)


class TriageResponse(BaseModel):
    decision: str = Field(..., description="need_more_info or conclude")
    follow_up_question: str | None = Field(default=None)
    risk_level: str | None = Field(default=None, description="HIGH, MODERATE, or LOW")
    detected_symptoms: List[str] = Field(default_factory=list)
    recommendation: str | None = Field(default=None)
    reasoning: str | None = Field(default=None)
