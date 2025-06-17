from datetime import datetime, timedelta, UTC
import secrets
from typing import Optional
from uuid import UUID

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.app.core.settings import settings           # ← точковий імпорт
from backend.app.models import Admin
# або: from backend.app.core import settings  (якщо прописав у __init__.py)

from backend.app.models.entities import User
from backend.app.services.sessions.refresh_token import RefreshTokenService


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.rt_service = RefreshTokenService(db)

    # --- helpers ---------------------------------------------------------

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_ctx.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)

    # --- public API ------------------------------------------------------

    def authenticate(self, email: str, password: str) -> Optional[Admin]:
        admin = (
            self.db.query(Admin)
            .filter_by(email=email, is_deleted=False)
            .first()
        )
        if admin and self.verify_password(password, str(admin.password_hash)):
            return admin
        return None

    @staticmethod
    def create_access_token(user_id: str) -> tuple[str, int]:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_EXPIRE_MINUTES
        )
        payload = {"sub": str(user_id), "exp": int(expire.timestamp())}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)
        return token, settings.ACCESS_EXPIRE_MINUTES * 60

    def create_refresh_token(
        self, user_id: str, ip: Optional[str], ua: Optional[str]
    ) -> str:
        raw = secrets.token_urlsafe(48)
        self.rt_service.create(
            UUID(user_id), raw, ip, ua, ttl_days=settings.REFRESH_EXPIRE_DAYS
        )
        return raw