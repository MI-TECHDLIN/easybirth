"""Shared language and locale helpers."""
from __future__ import annotations

SUPPORTED_LANGUAGES = ("en", "sw")


def is_supported_language(code: str) -> bool:
    """Return whether a language code is supported by the app."""
    return code in SUPPORTED_LANGUAGES
