"""
Document validator.
Since files come via Telegram, here we only ensure
the value is not empty (actual file handled in bot layer).
"""

from typing import Tuple
from .base import ok, error


def validate_document(value: str) -> Tuple[bool, str]:
    if not value.strip():
        return error("errors.no_document")

    return ok()


__all__ = ["validate_document"]
