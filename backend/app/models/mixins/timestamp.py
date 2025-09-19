from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func


class TimeStampMixin:
    """
    Abstract base class that adds timestamp fields to models.

    Fields:
    - created_at: Automatically set to the current UTC time when the record is created.
    - updated_at: Automatically set to the current UTC time on creation and update.

    This mixin ensures consistent tracking of creation and modification times.
    """

    __abstract__ = True  # Prevents SQLAlchemy from mapping this class to a standalone table

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DB sets current time on insert
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # DB sets current time on insert
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )
