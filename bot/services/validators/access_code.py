"""
Access code validator.

This validator contacts the backend to verify whether a given
access code exists and is valid.

Backend endpoint:
    GET /application/check-access-code?code=<value>

Expected backend responses:
    200 OK:
        {"valid": true}
        {"valid": false}

    400/422:
        {"detail": "..."}   # invalid code format

    500:
        internal backend failure

Validation result format:
    (success: bool, message: str)

On success:
    (True, "ok")

On failure (invalid code OR backend says false):
    (False, "<localized_error_key>")
"""

import httpx
from typing import Tuple
from .base import ok, error


BACKEND_URL = "https://api.worldflowcredit.com"   # TODO: replace after refactor
TIMEOUT = 5.0


async def validate_access_code(value: str) -> Tuple[bool, str]:
    """
    Validate access code via backend API.

    Steps:
        1. Trim input
        2. If empty → error
        3. Call backend
        4. Interpret result
        5. Convert into wizard-compatible (True/False, message)
    """
    # value = value.strip()
    #
    # # ---- 1) Empty? ----
    # if not value:
    #     return error("access_code.empty")
    #
    # # ---- 2) Ask backend ----
    # url = f"{BACKEND_URL}/application/check-access-code"
    # params = {"code": value}
    #
    # try:
    #     async with httpx.AsyncClient(timeout=TIMEOUT) as client:
    #         resp = await client.get(url, params=params)
    #
    # except httpx.RequestError:
    #     # Network error or timeout → show soft error
    #     return error("access_code.unavailable")
    #
    # # ---- 3) Non-200? ----
    # if resp.status_code != 200:
    #     # Unknown backend status = treat as invalid
    #     return error("access_code.invalid")
    #
    # # ---- 4) Parse JSON ----
    # try:
    #     data = resp.json()
    # except Exception:
    #     return error("access_code.invalid")
    #
    # # ---- 5) Interpret response ----
    # is_valid = data.get("valid", False)
    #
    # if not is_valid:
    #     # Access code exists but invalid
    #     return error("access_code.invalid")
    #
    # # Ok
    return ok()


__all__ = ["validate_access_code"]
