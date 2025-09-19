"""
Authentication request schemas initializer.

This module consolidates Pydantic models related to authentication input data,
such as login, registration, and password reset requests.

Usage:
    from backend.app.schemas.auth import (
        LoginRequest,
        RegisterRequest,
        ResetPasswordRequest,
        ResetPasswordConfirm,
    )

Exports:
    - LoginRequest: Schema for user login (email + password).
    - RegisterRequest: Schema for user registration (email + password).
    - ResetPasswordRequest: Schema for initiating password reset (email only).
    - ResetPasswordConfirm: Schema for confirming password reset (token + new password).
"""

from .login_request import LoginRequest
from .register_request import RegisterRequest
from .reset_password_request import ResetPasswordRequest
from .reset_password_confirm import ResetPasswordConfirm

__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "ResetPasswordRequest",
    "ResetPasswordConfirm",
]
