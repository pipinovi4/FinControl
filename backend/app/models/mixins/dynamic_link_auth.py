from datetime import datetime, timedelta, UTC
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class DynamicLinkAuthMixin:
    """
    Mixin for authentication via dynamic login links.

    This mixin provides fields and methods for one-time, time-limited login sessions
    that can be safely sent via external channels (e.g., Telegram bot, email).

    Components:
    - `dynamic_login_token`: hashed one-time token used for login validation
    - `expires_at`: expiration datetime after which the token is invalid
    - `is_used`: flag indicating whether the token has already been used
    """

    __abstract__ = True

    # Hashed login token (e.g., SHA-256), nullable so it can be cleared after use
    dynamic_login_token: Mapped[Optional[str]] = mapped_column(
        String(64),  # SHA-256 hex digest length is always 64 characters
        nullable=True  # Token is nullable to allow removal after use
    )

    # Expiration datetime (e.g., 5 minutes after generation); uses timezone-aware UTC datetime
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # Ensure proper comparison with timezone-aware datetime
        default=lambda: datetime.now(UTC) + timedelta(minutes=5),  # Default expiration time: 5 minutes
        nullable=False
    )

    # Token usage flag — once used, token cannot be reused
    is_used: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False  # Initially, the token has not been used
    )
