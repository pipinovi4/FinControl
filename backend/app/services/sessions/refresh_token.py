from datetime import datetime, UTC, timedelta
from uuid import UUID
from hashlib import sha256
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import secrets

from backend.app.models.sessions.refresh_token import RefreshToken
from backend.app.utils.decorators import handle_exceptions


class RefreshTokenService:
    """
    Async service for managing refresh token records in the database.

    Supports creation, validation, revocation, and rotation of secure refresh tokens.
    Designed for use in FastAPI async workflows.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the service with an async database session.

        Args:
            db (AsyncSession): The active async DB session.
        """
        self.db = db

    @staticmethod
    def hash(raw: str) -> str:
        """
        Hash a raw refresh token using SHA-256.

        Args:
            raw (str): The plain text token.

        Returns:
            str: SHA-256 hash of the token.
        """
        return sha256(raw.encode()).hexdigest()

    @handle_exceptions()
    async def create(
        self,
        user_id: UUID,
        raw_token: str,
        created_from_ip: str | None,
        user_agent: str | None,
        ttl_days: int = 30,
    ):
        """
        Create and persist a new refresh token.

        Args:
            user_id (UUID): ID of the user.
            raw_token (str): Raw token to hash.
            created_from_ip (Optional[str]): IP address.
            user_agent (Optional[str]): User-Agent string.
            ttl_days (int): Token lifespan in days.
        """
        token_row = RefreshToken(
            user_id=user_id,
            token_hash=self.hash(raw_token),
            created_from_ip=created_from_ip,
            user_agent=user_agent,
            expires_at=datetime.now(UTC) + timedelta(days=ttl_days),
            is_active=True,
        )
        self.db.add(token_row)
        await self.db.commit()
        await self.db.refresh(token_row)

    @handle_exceptions()
    async def revoke(self, token_hash: str) -> None:
        """
        Mark a token as inactive (soft revoke) by its hash.

        Args:
            token_hash (str): Hashed token string.
        """
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .values(is_active=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions(default_return=None)
    async def verify(self, raw_token: str) -> RefreshToken | None:
        """
        Check if a token is active and not expired.

        Args:
            raw_token (str): Raw token string.

        Returns:
            Optional[RefreshToken]: Token object if valid, else None.
        """
        hashed = self.hash(raw_token)

        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == hashed,
            RefreshToken.is_active.is_(True),
            RefreshToken.expires_at > datetime.now(UTC),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    @handle_exceptions()
    async def rotate(
        self,
        stored_token: RefreshToken,
        ip: str | None,
        ua: str | None,
        ttl_days: int = 30,
    ) -> str:
        """
        Soft-revoke the existing token and issue a new one.

        Args:
            stored_token (RefreshToken): The token being rotated.
            ip (Optional[str]): New client IP.
            ua (Optional[str]): New User-Agent.
            ttl_days (int): New token lifespan.

        Returns:
            str: The new raw token.
        """
        stored_token.is_active = False
        self.db.add(stored_token)

        raw_token = secrets.token_urlsafe(48)
        hashed = self.hash(raw_token)

        new_token = RefreshToken(
            user_id=stored_token.user_id,
            token_hash=hashed,
            created_from_ip=ip,
            user_agent=ua,
            expires_at=datetime.now(UTC) + timedelta(days=ttl_days),
            is_active=True,
        )
        self.db.add(new_token)
        await self.db.commit()

        return raw_token
