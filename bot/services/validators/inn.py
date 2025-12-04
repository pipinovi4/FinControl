"""
Validate Russian INN: 10 or 12 digits.
"""

import re
from typing import Tuple
from .base import ok, error


async def validate_inn_ru(value: str) -> Tuple[bool, str]:
    v = value.strip()

    if not re.fullmatch(r"\d{10}|\d{12}", v):
        return error("errors.invalid_inn")

    return ok()


__all__ = ["validate_inn_ru"]
