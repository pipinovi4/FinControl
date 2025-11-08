from datetime import datetime, UTC
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets

from app.core.settings import settings
from app.models.sessions import RefreshToken
from app.services.sessions.refresh_token import RefreshTokenService
from app.utils.decorators import handle_exceptions


class RefreshService:
    """
    High-level abstraction for managing refresh token creation and validation.

    This service wraps the lower-level RefreshTokenService and adds logic
    for raw token generation, hashing, and single-use consumption with IP/UA checks.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the service with an active async DB session and
        prepare the internal RefreshTokenService handler.

        Args:
            db (AsyncSession): The async database session.
        """
        self.db = db
        self.rt_service = RefreshTokenService(db)

    async def create(self, user_id: str, ip: Optional[str], ua: Optional[str]) -> str:
        """
        Generate and persist a new refresh token for a given user.
        Returns the raw (unhashed) token that will be sent to the client.

        Args:
            user_id (str): User UUID as a string.
            ip (Optional[str]): Client IP address.
            ua (Optional[str]): Client User-Agent string.

        Returns:
            str: The generated raw refresh token.
        """
        raw = secrets.token_urlsafe(48)
        await self.rt_service.create(
            UUID(user_id), raw, ip, ua, ttl_days=settings.REFRESH_EXPIRE_DAYS
        )
        return raw

    @handle_exceptions()
    async def consume(self, token: str, created_from_ip: Optional[str], user_agent: Optional[str]) -> Optional[RefreshToken]:
        """
        Validate and consume a refresh token if it's active and matches the
        given IP and User-Agent. This marks the token as used.

        Args:
            token (str): The raw refresh token from the client.
            created_from_ip (Optional[str]): IP address of the request (if available).
            user_agent (Optional[str]): User-Agent header of the request (if available).

        Returns:
            Optional[RefreshToken]: The matched and consumed RefreshToken instance,
            or None if the token is invalid, expired, or doesn't match.
        """
        # Hash the raw token to match against the stored token_hash
        hashed = self.rt_service.hash(token)

        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == hashed,
            RefreshToken.is_active.is_(True),
            RefreshToken.created_from_ip == created_from_ip,
            RefreshToken.user_agent == user_agent
        )

        result = await self.db.execute(stmt)
        rt = result.scalar_one_or_none()

        # Check if token is found and not expired
        if not rt or rt.expires_at < datetime.now(UTC):
            return None

        # Mark token as used and persist the change
        rt.is_used = True
        await self.db.commit()
        return rt
