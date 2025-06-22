# backend/app/services/auth/utils.py
import secrets
from uuid import UUID

async def generate_token_pair(user_id: UUID, db, ip: str, ua: str):
    from .access_token import AccessTokenService
    from .refresh_token import RefreshTokenService

    access_service = AccessTokenService()
    refresh_service = RefreshTokenService(db)

    access, ttl = access_service.create(str(user_id))
    raw_token = secrets.token_urlsafe(48)
    await refresh_service.create(user_id, raw_token, ip, ua)

    return access, raw_token, ttl
