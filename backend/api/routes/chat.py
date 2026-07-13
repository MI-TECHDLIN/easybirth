"""Chat routes for the API service."""
from __future__ import annotations

from fastapi import APIRouter

from api.schemas.chat import ChatRequest, ChatResponse
from api.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
service = ChatService()


@router.post("", response_model=ChatResponse)
def create_chat(payload: ChatRequest) -> ChatResponse:
    return service.respond(payload)
