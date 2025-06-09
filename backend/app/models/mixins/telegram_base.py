from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class TelegramMixin:
    """
    Mixin for storing Telegram identity fields.

    Fields:
    - telegram_id: Permanent unique Telegram user ID (string format).
    - telegram_username: Optional Telegram username (can be changed by the user).

    Notes:
    - telegram_id is required and indexed for fast lookups.
    - telegram_username may be null since not all users have it.
    """

    __abstract__ = True

    telegram_id: Mapped[str] = mapped_column(
        String(32),         # Safe upper bound for Telegram IDs as strings
        unique=True,
        nullable=False,
        index=True
    )

    telegram_username: Mapped[str] = mapped_column(
        String(255),        # Telegram usernames can be up to ~32 chars
        unique=True,
        nullable=True       # Usernames are optional and can be changed
    )
