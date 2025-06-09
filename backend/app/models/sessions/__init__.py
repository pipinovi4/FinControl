"""
Sessions package initializer.

This module re-exports session and token-related models so they can be
imported directly from 'backend.app.models.sessions'.
"""

# RefreshToken model for tracking per-device refresh tokens
from backend.app.models.sessions.refresh_token import RefreshToken

# Public API of the sessions package
__all__ = [
    "RefreshToken",
]
