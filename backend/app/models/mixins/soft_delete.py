from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime
from typing import Optional
import datetime


class SoftDeleteMixin:
    """
    Mixin that adds a soft delete flag to a SQLAlchemy model.
    """

    __abstract__ = True  # Ensures this mixin does not become its own table

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        info={"description": "Soft delete flag"}
    )

    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
        info={"description": "When object was marked as deleted"}
    )
