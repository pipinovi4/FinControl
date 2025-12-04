"""
Address validator — minimal format check.
Must be 5+ chars.
"""

from typing import Tuple
from .base import ok, error


def validate_address(value: str) -> Tuple[bool, str]:
    if len(value.strip()) < 5:
        return error("errors.invalid_address")

    return ok()


__all__ = ["validate_address"]
