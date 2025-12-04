"""
Generic ID number validator.
Checks length and alphanumerics.
"""

import re
from typing import Tuple
from .base import ok, error


async def validate_id_number(value: str) -> Tuple[bool, str]:
    v = value.strip()

    if not re.fullmatch(r"[A-Za-z0-9\-]{4,20}", v):
        return error("errors.invalid_id")

    return ok()


__all__ = ["validate_id_number"]
