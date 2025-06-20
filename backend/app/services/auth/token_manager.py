from datetime import datetime, timedelta, UTC
from typing import Any, Literal

import jwt  # PyJWT
from uuid import UUID

from backend.app.core.settings import settings

# Allowed token types — used to differentiate JWT purpose
TokenType = Literal["access", "refresh", "reset"]


class TokenManager:
    """
    Minimalist JWT handler for access, refresh, and password reset tokens.

    Encodes and decodes JWTs with a built-in structure that includes:
    - `sub`: subject (typically user ID)
    - `type`: token category (access | refresh | reset)
    - `exp`: expiration timestamp (UTC)
    - `iat`: issued-at timestamp (UTC)

    Usage:
        TokenManager.encode({"sub": str(user.id)}, token_type="access")
        TokenManager.decode(token, expected_type="access")
    """

    _secret = settings.JWT_SECRET
    _alg = "HS256"

    # Default expiration (in minutes) per token type
    _default_ttl = {
        "access": 15,              # 15 minutes
        "refresh": 60 * 24 * 30,   # 30 days
        "reset": 30,               # 30 minutes
    }

    @classmethod
    def encode(
        cls,
        payload: dict[str, Any],
        token_type: TokenType = "access",
        ttl_minutes: int | None = None,
    ) -> str:
        """
        Encode a JWT with additional metadata.

        Args:
            payload (dict): Custom payload data (must include `sub` manually).
            token_type (str): Token category. Affects default TTL.
            ttl_minutes (int, optional): Time-to-live override in minutes.

        Returns:
            str: Encoded JWT string.
        """
        ttl = ttl_minutes or cls._default_ttl[token_type]
        now = datetime.now(UTC)
        claims = {
            **payload,
            "type": token_type,
            "iat": now,
            "exp": now + timedelta(minutes=ttl),
        }
        return jwt.encode(claims, cls._secret, algorithm=cls._alg)

    @classmethod
    def decode(
        cls,
        token: str,
        expected_type: TokenType | None = None,
    ) -> dict[str, Any]:
        """
        Decode and verify a JWT.

        Args:
            token (str): Encoded JWT.
            expected_type (str, optional): If set, verifies the token type matches.

        Returns:
            dict: Decoded JWT payload.

        Raises:
            ValueError: If the token is expired or invalid.
        """
        try:
            data = jwt.decode(token, cls._secret, algorithms=[cls._alg])
            if expected_type and data.get("type") != expected_type:
                raise jwt.InvalidTokenError(f"Unexpected token type: {data.get('type')}")
            return data
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")
