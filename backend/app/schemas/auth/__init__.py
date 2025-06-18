"""
Authentication request schemas initializer.

This module consolidates Pydantic models related to authentication input data,
such as login and registration requests.

Usage:
    from backend.app.schemas.auth import LoginRequest, RegisterRequest

Exports:
    - LoginRequest: Schema for user login (email + password).
    - RegisterRequest: Schema for user registration (email + password).
"""

from .login_request import LoginRequest        # Login input: email + password
from .register_request import RegisterRequest  # Register input: email + password

__all__ = [
    "LoginRequest",
    "RegisterRequest",
]
