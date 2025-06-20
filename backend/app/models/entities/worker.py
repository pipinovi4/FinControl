from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey
from backend.app.models.entities.user import User
from backend.app.models.mixins import TimeStampAuthMixin, DynamicLinkAuthMixin


class Worker(User, TimeStampAuthMixin, DynamicLinkAuthMixin):
    """
    Represents an internal employee who manages client applications
    and interacts with the system via the admin panel.

    Inherits:
    - User: Base class with UUID, Telegram ID, timestamps, etc.
    - AuthMixin: Adds email + password_hash authentication
    - TimeStampAuthMixin: Tracks last login timestamp
    - DynamicLinkAuthMixin: Enables one-time secure login via dynamic links

    Worker has full access to client data they manage and is
    distinguishable by `polymorphic_identity='worker'`.
    """

    __tablename__ = "workers"

    # Primary key UUID, inherits from User table via foreign key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # System-wide internal login username (e.g., "john.smith")
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    # One-to-many relationship: this worker can have multiple clients
    clients: Mapped[list["Client"]] = relationship(
        "Client",
        back_populates="worker",
        foreign_keys="Client.worker_id",
        cascade="all"
    )

    # Used by SQLAlchemy's polymorphic system to identify the model
    __mapper_args__ = {
    "inherit_condition": (id == User.id),
        "polymorphic_identity": "worker",
    }

    def __repr__(self) -> str:
        # Developer-friendly string output
        return f"Worker(id={self.id}, username={self.username})"
