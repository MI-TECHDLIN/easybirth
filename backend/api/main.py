"""Application entrypoint for the EasyBirth API package."""
from __future__ import annotations

from typing import Any

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - fallback for minimal environments
    FastAPI = None


def create_app() -> dict[str, Any]:
    """Return a minimal application description used by the foundation setup."""
    return {"name": "easybirth-backend", "status": "initialized"}


if FastAPI is not None:
    app = FastAPI(title="EasyBirth Backend", version="0.1.0")

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}
else:  # pragma: no cover - exercised when FastAPI is absent
    app = None
