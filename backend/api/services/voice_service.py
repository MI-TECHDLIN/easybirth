"""Placeholder voice service."""
from __future__ import annotations

from api.schemas.voice import VoiceRequest, VoiceResponse


class VoiceService:
    def transcribe(self, payload: VoiceRequest) -> VoiceResponse:
        return VoiceResponse(
            transcript="Placeholder transcript",
            language=payload.language,
            status="queued",
        )
