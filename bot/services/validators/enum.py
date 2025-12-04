"""
Enum validator.

Validates that the user input matches one of allowed options.
Used for steps that offer only button selections.
"""

from typing import Tuple, List
from .base import ok, error


async def validate_enum(value: str, allowed: List[str]) -> Tuple[bool, str]:
    if value in allowed:
        return ok()

    return error(
        "Пожалуйста, выберите один из вариантов, используя кнопки ниже."
    )


__all__ = ["validate_enum"]
