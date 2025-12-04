"""
Income validator — expects numeric income (net).
"""

import re
from typing import Tuple
from .base import ok, error


def validate_income(value: str) -> Tuple[bool, str]:
    v = value.replace(" ", "").strip()

    if not re.fullmatch(r"\d{2,10}", v):
        return error("errors.invalid_income")

    return ok()


__all__ = ["validate_income"]
