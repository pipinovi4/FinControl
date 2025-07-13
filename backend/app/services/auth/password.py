# backend/app/services/auth/password_service.py
from __future__ import annotations

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from backend.app.models.entities.user import User   # базова модель

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordService:
    """Hash / verify / authenticate any polymorphic User."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------- static helpers ----------

    @staticmethod
    def hash(password: str) -> str:
        """Return bcrypt-hash for given plain password."""
        return pwd_ctx.hash(password)

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        """Check plain password against stored hash."""
        return pwd_ctx.verify(plain, hashed)

    # ---------- main method ----------

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> Optional[User]:
        """
        Returns polymorphic `User` instance (Admin | Worker | Broker | Client)
        if credentials are valid, otherwise `None`.
        """
        stmt = (
            select(User)
            .where(
                User.email == email,
                User.is_deleted.is_(False)   # ignore soft-deleted users
            )
            .limit(1)
        )
        result = await self.db.execute(stmt)
        user: User | None = result.scalar_one_or_none()

        if user and self.verify(password, user.password_hash):
            return user     # automatically loaded as proper subclass
        return None
