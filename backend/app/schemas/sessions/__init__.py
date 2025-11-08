"""
Session-related schemas initializer.

This module provides a unified import path for all schemas related to session
management, including refresh tokens and access/refresh token pairs.

Usage:
    from app.schemas.sessions import TokenPair, RefreshRequest, RefreshTokenSchema

Exports:
    - TokenPair: Access and refresh token response model.
    - RefreshRequest: Request model used to obtain a new access token.
    - RefreshTokenSchema: Internal schema for database representation of refresh tokens.
"""

from .refresh_token import RefreshTokenSchema  # Pydantic schema for refresh token DB representation
from .token_pair import TokenPair              # Response schema containing access & refresh tokens
from .refresh_request import RefreshRequest    # Request schema used for refreshing tokens

__all__ = [
    "RefreshTokenSchema",
    "TokenPair",
    "RefreshRequest",
]
