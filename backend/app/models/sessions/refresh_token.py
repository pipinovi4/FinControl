from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta, UTC
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
import uuid

from backend.db.session import Base
from backend.app.models.mixins import UUIDMixin, TimeStampMixin


class RefreshToken(Base, UUIDMixin, TimeStampMixin):
    """
    Persistent storage for JWT refresh tokens.

    Each record represents one “session” or long-lived credential
    that can be used to issue new access tokens.

    Inherits:
      - UUIDMixin:         adds `id: UUID` primary key
      - TimeStampMixin:    adds `created_at` & `updated_at` timestamps
    """

    __tablename__ = "refresh_tokens"

    # Link back to the owning user; cascade deletes so tokens
    # are removed automatically when the user is deleted.
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy="joined",
    )

    # The opaque refresh token string (or its hash).
    # Unique so the same token cannot be reused by two sessions.
    token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    # IP address from which the token was issued.
    # Useful for security/audit purposes.
    ip: Mapped[Optional[str]] = mapped_column(
        String(45),  # covers both IPv4 and IPv6 textual formats
        nullable=True,
    )

    # User-agent string of the client that requested the token.
    # Helps you identify and revoke suspicious or stale sessions.
    user_agent: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    # When this refresh token expires and can no longer be used.
    # Default is 30 days from creation.
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(days=30),
        nullable=False,
    )

    # Soft-flag to invalidate the token without deleting the row.
    # You can revoke a single session by setting `is_active=False`.
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
