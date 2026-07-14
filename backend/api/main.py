"""FastAPI application entrypoint for the EasyBirth backend."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import settings
from api.routes.chat import router as chat_router
from api.routes.explainability import router as explainability_router
from api.routes.health import router as health_router
from api.routes.risk_assessments import router as risk_router
from api.routes.triage import router as triage_router
from api.routes.voice import router as voice_router

app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(risk_router, prefix="/api/v1")
app.include_router(triage_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(explainability_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "EasyBirth backend is running"}
