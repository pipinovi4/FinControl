import secrets
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from backend.app.core.settings import settings
from backend.app.models.sessions import RefreshToken
from backend.app.services.sessions.refresh_token import RefreshTokenService


class RefreshService:
    def __init__(self, db: Session):
        self.db = db
        self.rt_service = RefreshTokenService(db)

    def create(self, user_id: str, ip: Optional[str], ua: Optional[str]) -> str:
        raw = secrets.token_urlsafe(48)
        self.rt_service.create(
            UUID(user_id), raw, ip, ua, ttl_days=settings.REFRESH_EXPIRE_DAYS
        )
        return raw

    def consume(self, token: str, ip: str|None, ua: str|None) -> RefreshToken|None:
        rt = (self.db.query(RefreshToken)
                  .filter_by(token=token, is_used=False, ip=ip, ua=ua)
                  .first())
        if not rt or rt.expires_at < datetime.now(UTC):
            return None
        rt.is_used = True; self.db.commit()
        return rt
