import re

PHONE_REGEX = re.compile(r"^\+?[0-9\s\-\(\)]{7,20}$")


def validate_phone(value: str):
    v = value.strip().replace(" ", "").replace("-", "")

    if not v.startswith("+"):
        v = "+" + v

    if not PHONE_REGEX.match(v):
        return False, "invalid_phone"

    if len(v) < 8:
        return False, "invalid_phone"

    return True, None


__all__ = ["validate_phone"]
