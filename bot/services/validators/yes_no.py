"""
Yes/No validator.

Used for binary steps where only 'Yes' or 'No' buttons are allowed.
"""

from typing import Tuple
from .base import ok, error


def validate_yes_no(value: str) -> Tuple[bool, str]:
    if value in ("Yes", "No"):
        return ok()

    return error("Пожалуйста, нажмите кнопку «Да» или «Нет».")


__all__ = ["validate_yes_no"]
