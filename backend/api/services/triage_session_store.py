"""Simple session store for preserving triage conversation state across requests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from api.schemas.triage import ConversationTurn

STORE_PATH = Path(__file__).resolve().parent.parent / "data" / "triage_sessions.json"

class TriageSessionStore:
    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, str]]] = {}
        self._store_path = STORE_PATH
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        self._load()

    def _load(self) -> None:
        if not self._store_path.exists():
            return
        try:
            raw = json.loads(self._store_path.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                self._store = {
                    session_id: [
                        {"role": turn.get("role", "user"), "content": turn.get("content", "")}
                        for turn in turns
                    ]
                    for session_id, turns in raw.items()
                    if isinstance(turns, list)
                }
        except Exception:
            self._store = {}

    def _persist(self) -> None:
        self._store_path.write_text(
            json.dumps(self._store, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_history(self, session_id: str) -> list[ConversationTurn]:
        return [ConversationTurn(**turn) for turn in self._store.get(session_id, [])]

    def save_history(self, session_id: str, history: list[ConversationTurn]) -> None:
        self._store[session_id] = [turn.model_dump() for turn in history]
        self._persist()

store = TriageSessionStore()
