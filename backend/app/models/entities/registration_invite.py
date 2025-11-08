# backend/app/models/entities/registration_invite.py
import uuid

from datetime import datetime, timedelta, UTC
from hashlib import sha256
from secrets import token_urlsafe
from uuid import uuid4

from sqlalchemy import String, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from db.session import Base

from app.permissions import PermissionRole

class RegistrationInvite(Base):
    __tablename__ = "registration_invites"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    # зберігаємо тільки HASH токена
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    role: Mapped[PermissionRole] = mapped_column(Enum(PermissionRole), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC) + timedelta(days=1),
        nullable=False,
    )
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ─ helper для сервісу ─
    @staticmethod
    def make_token() -> tuple[str, str]:
        raw = token_urlsafe(32)
        return raw, sha256(raw.encode()).hexdigest()
