from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
from datetime import datetime, UTC
from typing import Sequence, cast, TypeVar
from pydantic import EmailStr

from backend.app.models.entities.user import User
from backend.app.permissions import PermissionRole
from backend.app.services.auth import PasswordService
from backend.app.utils.decorators import handle_exceptions

UserT = TypeVar("UserT", bound=User)


class UserService:
    """
    UserService handles operations on User entities: fetch, update, soft/hard delete, and restore.

    Methods:
        get_user_by_id(user_id): Fetch user by UUID, raise 404 if not found.
        get_user_by_telegram_id(telegram_id): Fetch user by Telegram ID.
        get_all(): Return all active (non-deleted) users.
        get_all_soft_deleted(): Return users marked as deleted.
        get_users_by_role(role): Return all active users with given role.
        update_last_login(user_id): Update user's last login timestamp.
        update_user(user_id, updates): Update user fields from a dictionary.
        soft_delete(user_id): Soft-delete user (set is_deleted=True).
        restore(user_id): Restore a soft-deleted user.
        delete_user(user_id): Hard delete user from database.
    """
    def __init__(self, db: AsyncSession):
        # Accepts an async SQLAlchemy session for database operations
        self.db = db

    # --- GETTERS ---

    @handle_exceptions(raise_404=True)
    async def get_user_by_id(self, user_id: UUID) -> UserT | None:
        # Find a user by UUID (only if not soft-deleted)
        stmt = select(User).where(User.id == user_id, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return cast(UserT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_user_by_telegram_id(self, telegram_id: str) -> UserT | None:
        # Get a user by their Telegram ID
        stmt = select(User).where(User.telegram_id == telegram_id, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return cast(UserT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_user_by_email(self, email: EmailStr):
        # Get a user by email address
        stmt = select(User).where(User.email == email, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return cast(UserT, result.scalar_one_or_none())

    @handle_exceptions(default_return=[])
    async def get_all_users(self) -> Sequence[UserT]:
        # Get all active (not deleted) users
        stmt = select(User).where(User.is_deleted == False)
        result = await self.db.execute(stmt)
        return cast(Sequence[UserT], result.scalars().all())

    @handle_exceptions(default_return=[])
    async def get_all_soft_deleted(self) -> Sequence[UserT]:
        # Get all users marked as deleted (soft delete)
        stmt = select(User).where(User.is_deleted == True)
        result = await self.db.execute(stmt)
        return cast(Sequence[UserT], result.scalars().all())

    @handle_exceptions(default_return=[])
    async def get_users_by_role(self, role: PermissionRole) -> Sequence[UserT]:
        # Get all users of a specific role (only active ones)
        stmt = select(User).where(User.role == role, User.is_deleted == False)
        result = await self.db.execute(stmt)
        return cast(Sequence[UserT], result.scalars().all())

    # --- UPDATES ---

    @handle_exceptions()
    async def update_last_login(self, user_id: UUID) -> None:
        # Update the user's last login timestamp
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        user.last_login = datetime.now(UTC)
        await self.db.commit()

    @handle_exceptions()
    async def update_user(self, user_id: UUID, updates: dict) -> UserT:
        # Update user's fields using a dictionary of new values
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        for key, value in updates.items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    @handle_exceptions()
    async def update_password(self, user_id: UUID, new_password: str) -> UserT | None:
        # Update the user's password (hashed before saving)
        user = await self.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        user.password_hash = PasswordService.hash(new_password)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # --- SOFT DELETE / RESTORE ---

    @handle_exceptions()
    async def soft_delete(self, user_id: UUID) -> None:
        # Soft-delete: mark user as deleted without removing from DB
        stmt = update(User).where(User.id == user_id).values(
            is_deleted=True, deleted_at=datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def restore(self, user_id: UUID) -> None:
        # Restore a soft-deleted user
        stmt = update(User).where(User.id == user_id).values(
            is_deleted=False, deleted_at=None
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # --- HARD DELETE ---

    @handle_exceptions()
    async def delete_user(self, user_id: UUID) -> UserT:
        # Permanently remove user from database (cannot be restored)
        user = await self.get_user_by_id(user_id)
        await self.db.delete(user)
        await self.db.commit()
        return user
