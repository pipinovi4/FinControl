"""Validation helpers (English docstrings, Russian prompts stay elsewhere)."""
import re
from datetime import datetime

def email(value: str) -> bool:
    """Return True iff *value* looks like an email."""
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value) is not None

def phone(value: str) -> bool:
    """+380991234567 / 0991234567 – 10‑15 digits allowed."""
    return re.match(r"^\+?\d{10,15}$", value) is not None

def date_ddmmyyyy(value: str) -> bool:
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def numeric(value: str) -> bool:
    return value.replace(" ", "").isdigit()