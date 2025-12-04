"""
Phone number validator.
Accepts digits, optional "+", 7–20 characters.
"""

import re
from typing import Tuple
from .base import ok, error


async def validate_phone(value: str) -> Tuple[bool, str]:
    v = value.strip()

    if not v:
        return error("errors.empty")

    pattern = r"^\+?\d{7,20}$"
    if not re.match(pattern, v):
        return error("errors.invalid_phone")

    return ok()


__all__ = ["validate_phone"]
