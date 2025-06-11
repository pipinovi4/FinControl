"""
Session-related schemas initializer.

Exposes schemas related to authentication sessions and token management.
Use this module to import session-related models from a unified entry point.
"""

from .RefreshToken import RefreshToken  # Pydantic schema for refresh token management

# Public API of the sessions schema package
__all__ = [
    "RefreshToken",
]
