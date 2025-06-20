from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

from backend.app.models.entities import User
from backend.app.models.mixins import TimeStampAuthMixin


class Broker(User, TimeStampAuthMixin):
    """
    Broker model — represents an external partner with limited read-only access.

    Inherits:
    - User: base user data including Telegram ID, role, etc.
    - AuthMixin: provides email + password_hash authentication
    - TimeStampAuthMixin: tracks last login datetime
    """

    __tablename__ = "brokers"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        info={"description": "Name of the broker's company"}
    )

    region: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
        info={"description": "List of regions where the broker is active"}
    )

    clients: Mapped[list["Client"]] = relationship(
        "Client",
        back_populates="broker",
        foreign_keys="Client.broker_id",
        cascade="all"
    )

    __mapper_args__ = {
        "polymorphic_identity": "broker",
        "inherit_condition": (id == User.id),
    }

    def __repr__(self) -> str:
        return f"<Broker id={self.id}, company={self.company_name}>"
