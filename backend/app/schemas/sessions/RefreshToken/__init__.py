"""
Namespace wrapper for accessing RefreshToken-related schemas.

This class groups together different representations of the RefreshToken schema
(e.g., base for internal use, out for response models) under a single access point.

Usage:
    from backend.app.schemas.sessions import RefreshToken

    token_base = RefreshToken.base(...)
    token_out = RefreshToken.out.from_orm(...)

This improves code readability and centralizes schema access.
"""

from .base import RefreshTokenBase  # Base schema for internal logic (e.g., DB operations)
from .out import RefreshTokenOut    # Output schema used in API responses

class RefreshToken:
    base = RefreshTokenBase
    out = RefreshTokenOut
