# backend/app/services/auth_service.py
from datetime import datetime, timedelta, UTC
import secrets
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.models.entities import User
from backend.app.services.sessions.refresh_token import RefreshTokenService
# from backend.app.dependencies import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.rt_service = RefreshTokenService(db)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.db.query(User).filter_by(email=email, is_deleted=False).first()
        if user and self.verify_password(password, user.password_hash):
            return user
        return None

    @staticmethod
    def create_access_token(user_id: str) -> tuple[str,int]:
        expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES)
        payload = {"sub": user_id, "exp": expire.timestamp()}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)
        return token, settings.ACCESS_EXPIRE_MINUTES * 60

    def create_refresh_token(self, user_id: str, ip: str | None, ua: str | None) -> str:
        raw = secrets.token_urlsafe(48)
        self.rt_service.create(UUID(user_id), raw, ip, ua, ttl_days=settings.REFRESH_EXPIRE_DAYS)
        return raw
