"""Voice processing schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceRequest(BaseModel):
    audio_url: str = Field(...)
    language: str = Field(default="en")


class VoiceResponse(BaseModel):
    transcript: str = Field(default="Placeholder transcript")
    language: str = Field(default="en")
    status: str = Field(default="queued")
