from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import text
import uuid

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
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,                         # Python-side (зручно в коді)
        server_default=text("gen_random_uuid()"),  # DB-side (надійно й уніфіковано)
        nullable=False,
    )
