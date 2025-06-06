from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class TelegramMixin:
    telegram_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    telegram_username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
