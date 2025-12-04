"""
Date validator – expects DD.MM.YYYY.
Checks numeric range and calendar validity.
"""

from datetime import datetime
from typing import Tuple
from .base import ok, error


async def validate_date(value: str) -> Tuple[bool, str]:
    v = value.strip()

    try:
        datetime.strptime(v, "%d.%m.%Y")
        return ok()
    except Exception:
        return error("errors.invalid_date")


__all__ = ["validate_date"]
