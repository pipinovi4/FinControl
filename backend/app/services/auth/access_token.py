import jwt
from datetime import datetime, timedelta, UTC
from backend.app.core.settings import settings

class AccessTokenService:
    @staticmethod
    def create(user_id: str) -> tuple[str, int]:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_EXPIRE_MINUTES
        )
        payload = {"sub": str(user_id), "exp": int(expire.timestamp())}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)
        return token, settings.ACCESS_EXPIRE_MINUTES * 60
