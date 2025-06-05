import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    """
    Abstract base class that replaces the default integer primary key with a UUID.

    Fields:
    - id: Primary key, automatically generated UUID (v4), unique and indexed.

    Benefits:
    - More secure and unpredictable than sequential integers.
    - Suitable for public-facing APIs and URL sharing.
    """

    __abstract__ = True  # Prevents SQLAlchemy from mapping this class to a standalone table

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),            # SQLAlchemy column type for native PostgreSQL UUID
        primary_key=True,              # Marks this field as primary key
        default=uuid.uuid4,            # Generates UUID automatically
        unique=True,                   # Ensures uniqueness in the database
        index=True,                    # Speeds up lookups by this field
        nullable=False
    )
