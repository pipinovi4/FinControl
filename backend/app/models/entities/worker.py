from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid
import enum

from backend.app.models.entities.user import User
from backend.app.models.mixins import TimeStampAuthMixin, DynamicLinkAuthMixin
from backend.app.permissions import PermissionRole

class DepartmentEnum(enum.Enum):
    HELIX = "Helix"
    UNION = "Union"

class Worker(User, TimeStampAuthMixin, DynamicLinkAuthMixin):
    """
    SQLAlchemy model representing a system worker (internal employee).

    Workers are responsible for managing client applications via the admin panel.
    They have full access to clients they oversee and may receive credits
    based on performance.

    Inherits:
    - User: Base user model with core fields (ID, role, etc.)
    - TimeStampAuthMixin: Adds tracking of `last_login_at` timestamp
    - DynamicLinkAuthMixin: Enables temporary access via a secure dynamic link
    """

    __tablename__ = "workers"

    # Primary key UUID, inherited from User table (joined-table inheritance)
    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Unique internal system username (e.g., john.smith)
    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    # One-to-many relationship: this worker can manage multiple clients
    clients: Mapped[list["Client"]] = relationship(
        "Client",
        back_populates="worker",
        foreign_keys="Client.worker_id",
        cascade="save-update, merge",
        passive_deletes=True,
    )

    department: Mapped[DepartmentEnum] = mapped_column(
        Enum(DepartmentEnum, name="department_enum"),
        nullable=True,
    )

    credits: Mapped[list["Credit"]] = relationship(
        "Credit",
        back_populates="worker",
        foreign_keys="Credit.worker_id",
        cascade="all",
        passive_deletes=True,
    )

    # Used to identify this subclass in SQLAlchemy polymorphic queries
    __mapper_args__ = {
        "inherit_condition": (id == User.id),
        "polymorphic_identity": PermissionRole.WORKER,
    }

    def __repr__(self) -> str:
        """
        Developer-friendly string representation.
        """
        return f"Worker(id={self.id}, username={self.username})"
