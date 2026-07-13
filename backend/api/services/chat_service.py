"""Placeholder chat service."""
from __future__ import annotations

from api.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def respond(self, payload: ChatRequest) -> ChatResponse:
        return ChatResponse(
            reply="Placeholder chat reply",
            language=payload.language,
            status="ok",
        )
