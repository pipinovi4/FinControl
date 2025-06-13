from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from datetime import datetime, timedelta, UTC
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from hashlib import sha256

from sqlalchemy.sql.schema import UniqueConstraint

from backend.db.session import Base
from backend.app.models.mixins import UUIDMixin, TimeStampMixin




class RefreshToken(Base, UUIDMixin, TimeStampMixin):
    __tablename__ = "refresh_tokens"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user = relationship("User", back_populates="refresh_tokens", lazy="selectin")

    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    created_from_ip: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent:     Mapped[Optional[str]] = mapped_column(String(255))

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(days=30),
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "token_hash", name="uix_user_token"),
    )

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return sha256(raw_token.encode()).hexdigest()
