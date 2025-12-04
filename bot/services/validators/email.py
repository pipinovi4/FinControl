"""
Email validator.
Basic RFC-compliant regexp.
"""

import re
from typing import Tuple
from .base import ok, error


EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


async def validate_email(value: str) -> Tuple[bool, str]:
    v = value.strip()

    if not v:
        return error("errors.empty")

    if not EMAIL_RE.match(v):
        return error("errors.invalid_email")

    return ok()


__all__ = ["validate_email"]
