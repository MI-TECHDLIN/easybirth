"""Shared typing aliases for the backend package."""
from __future__ import annotations

from typing import Any

JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None
