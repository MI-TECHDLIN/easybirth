"""Voice routes for the API service."""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas.voice import VoiceRequest, VoiceResponse
from api.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["voice"])
service = VoiceService()


@router.post("", response_model=VoiceResponse)
def process_voice(payload: VoiceRequest) -> VoiceResponse:
    return service.transcribe(payload)
