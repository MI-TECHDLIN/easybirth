"""Logging configuration helpers."""
from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return a module logger."""
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
    return logging.getLogger("easybirth")
