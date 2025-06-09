from .base import UserBase


class UserUpdate(UserBase):
    """
    Schema for updating an existing user.

    Fields are optional to allow partial updates.
    """
    telegram_username: str | None = None
    is_active: bool | None = None
