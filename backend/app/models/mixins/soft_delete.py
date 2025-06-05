from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean

class SoftDeleteMixin:
    """
    Adds a logical deletion flag for soft delete functionality.
    """
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
