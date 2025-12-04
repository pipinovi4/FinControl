"""
Base validator utilities.

Standardizes return format across all validators.

Each validator returns:
    (is_valid: bool, error_code: str)
"""

from typing import Tuple


def ok() -> Tuple[bool, str]:
    """Successful validation."""
    return True, ""


def error(code: str) -> Tuple[bool, str]:
    """
    Validation failed.

    Args:
        code: localization key, e.g. "errors.invalid_phone"
    """
    return False, code


__all__ = ["ok", "error"]