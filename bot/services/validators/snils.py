"""
Validate Russian SNILS format: XXX-XXX-XXX YY
"""

import re
from typing import Tuple
from .base import ok, error


PATTERN = r"^\d{3}-\d{3}-\d{3}\s\d{2}$"


async def validate_snils(value: str) -> Tuple[bool, str]:
    if not re.match(PATTERN, value.strip()):
        return error("errors.invalid_snils")

    return ok()


__all__ = ["validate_snils"]
