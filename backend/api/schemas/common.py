"""Common schemas for the API service."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ExplanationResponse(BaseModel):
    explanation: str = Field(default="Placeholder explanation")
    model_version: str = Field(default="0.1.0-dev")
