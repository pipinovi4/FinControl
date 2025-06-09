from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean


class SoftDeleteMixin:
    """
    Mixin that adds a soft delete flag to a SQLAlchemy model.

    This mixin is intended to be used in models where records should not be physically deleted
    from the database, but instead marked as 'deleted' logically.

    Field:
    - is_deleted (bool): When True, the record is considered deleted and should be excluded from normal queries.

    Notes:
    - This mixin does not implement any behavior or methods — it only defines the schema.
    - Filtering (e.g., `is_deleted=False`) should be applied at the query or service layer.
    - For performance, `index=True` is set to optimize soft delete filtering.
    - Combine with timestamp fields (e.g., `deleted_at`) for full audit trail if needed.
    - Marked as `__abstract__` to avoid being mapped as a standalone table.

    Example usage:
        class User(Base, SoftDeleteMixin):
            __tablename__ = "users"
            ...
    """

    __abstract__ = True  # Ensures this mixin does not become its own table

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,        # All new records are active by default
        nullable=False,       # Enforces explicit boolean value
        index=True            # Optimizes lookups for active records
    )
