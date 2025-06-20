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

from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, UTC
from typing import Sequence, cast, TypeVar

from backend.app.models.entities.user import User
from backend.app.permissions import PermissionRole
from backend.app.utils.decorators import handle_exceptions

UserT = TypeVar("UserT", bound=User)


class UserService:
    """Service for handling User-related DB logic."""

    def __init__(self, db: Session):
        """Initialize with a DB session."""
        self.db = db

    # --- GETTERS ---

    @handle_exceptions(raise_404=True)
    def get_user_by_id(self, user_id: UUID) -> UserT | None:
        return cast(UserT, self.db.query(User).filter_by(id=user_id, is_deleted=False).first())

    @handle_exceptions()
    def get_user_by_telegram_id(self, telegram_id: str) -> UserT | None:
        return cast(UserT, self.db.query(User).filter_by(telegram_id=telegram_id, is_deleted=False).first())

    @handle_exceptions(default_return=[])
    def get_all(self) -> Sequence[UserT]:
        return cast(Sequence[UserT], self.db.query(User).filter_by(is_deleted=False).all())

    @handle_exceptions(default_return=[])
    def get_all_soft_deleted(self) -> Sequence[UserT]:
        return cast(Sequence[UserT], self.db.query(User).filter_by(is_deleted=True).all())

    @handle_exceptions(default_return=[])
    def get_users_by_role(self, role: PermissionRole) -> Sequence[UserT]:
        return cast(Sequence[UserT], self.db.query(User).filter_by(role=role, is_deleted=False).all())

    # --- UPDATES ---

    @handle_exceptions()
    def update_last_login(self, user_id: UUID) -> None:
        self.db.query(User).filter_by(id=user_id).update({"last_login": datetime.now(UTC)})
        self.db.commit()

    @handle_exceptions()
    def update_user(self, user_id: UUID, updates: dict) -> UserT:
        user = self.get_user_by_id(user_id)
        for key, value in updates.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    # --- SOFT DELETE / RESTORE ---

    @handle_exceptions()
    def soft_delete(self, user_id: UUID) -> None:
        self.db.query(User).filter_by(id=user_id).update({
            "is_deleted": True,
            "deleted_at": datetime.utcnow()
        })
        self.db.commit()

    @handle_exceptions()
    def restore(self, user_id: UUID) -> None:
        self.db.query(User).filter_by(id=user_id).update({
            "is_deleted": False,
            "deleted_at": None
        })
        self.db.commit()

    # --- HARD DELETE ---

    @handle_exceptions()
    def delete_user(self, user_id: UUID) -> UserT:
        user = self.get_user_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
        return user
