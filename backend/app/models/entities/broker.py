from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from backend.app.models.entities.user import User
from backend.app.models.entities.credit import Credit # noqa 401
from backend.app.models.mixins import TimeStampAuthMixin
from backend.app.permissions import PermissionRole


class Broker(User, TimeStampAuthMixin):
    """
    SQLAlchemy model representing a broker entity.

    A broker is an external partner who submits clients to the platform and
    monitors their processing progress. Brokers usually have limited access rights.

    Inherits:
    - User: Provides base identification, contact info, and polymorphic role.
    - TimeStampAuthMixin: Adds `last_login_at` timestamp.
    """

    __tablename__ = "brokers"

    # Primary key inherited from users table (joined-table inheritance)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Optional company name the broker is associated with
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        info={"description": "Name of the broker's company"}
    )

    # List of regions (as strings) where the broker operates
    region: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
        info={"description": "List of regions where the broker is active"}
    )

    # One-to-many relationship: the broker can have many clients
    clients: Mapped[list["Client"]] = relationship(
        "Client",
        back_populates="broker",
        foreign_keys="Client.broker_id",
        cascade="all"
    )

    credits: Mapped[list["Credit"]] = relationship(
        "Credit", back_populates="broker", foreign_keys="Credit.broker_id", cascade="all, delete-orphan"
    )

    # SQLAlchemy discriminator config to distinguish this subclass of User
    __mapper_args__ = {
        "inherit_condition": (id == User.id),
        "polymorphic_identity": PermissionRole.BROKER,
    }

    def __repr__(self) -> str:
        """
        Developer-friendly string representation.
        """
        return f"<Broker id={self.id}, company={self.company_name}>"
