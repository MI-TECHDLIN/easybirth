"""Core configuration utilities for the API service."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration from environment variables.
    
    Uses Pydantic V2+ SettingsConfigDict pattern (backwards compatible with V3).
    """

    app_name: str = "easybirth-backend"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
