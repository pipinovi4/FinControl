"""
Full name validator.
At least 2 words, 2+ characters each.
"""

from typing import Tuple
from .base import ok, error


async def validate_full_name(value: str) -> Tuple[bool, str]:
    parts = value.strip().split()

    if len(parts) < 2:
        return error("errors.invalid_full_name")

    if any(len(p) < 2 for p in parts):
        return error("errors.invalid_full_name")

    return ok()


__all__ = ["validate_full_name"]
