"""Chat request and response schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    language: str = Field(default="en")


class ChatResponse(BaseModel):
    reply: str = Field(default="Placeholder chat reply")
    language: str = Field(default="en")
    status: str = Field(default="ok")
