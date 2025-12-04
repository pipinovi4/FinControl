"""
Loan amount validator.
Accepts integers 3–9 digits (e.g., 1000…999999999)
"""

import re
from typing import Tuple
from .base import ok, error


async def validate_amount(value: str) -> Tuple[bool, str]:
    v = value.replace(" ", "").strip()

    if not re.fullmatch(r"\d{3,9}", v):
        return error("errors.invalid_amount")

    return ok()


__all__ = ["validate_amount"]
