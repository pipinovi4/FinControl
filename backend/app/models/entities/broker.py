from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from backend.app.models import User
from backend.app.models.mixins import AuthMixin, TimeStampAuthMixin


class Broker(User, AuthMixin, TimeStampAuthMixin):
    """
    Broker model — represents an external partner with limited read-only access.

    Inherits:
    - User: base user data including Telegram ID, role, etc.
    - AuthMixin: provides email + password_hash authentication
    - TimeStampAuthMixin: tracks last login datetime
    """

    __tablename__ = "brokers"

    # Primary key mapped to base users.id (inherits from User)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Optional company name associated with the broker
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Name of the broker's company"
    )

    # Regions broker is responsible for — stored as a list of strings
    region: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
        comment="List of regions where the broker is active"
    )

    __mapper_args__ = {
        "polymorphic_identity": "broker"  # Used for polymorphic loading
    }

    def __repr__(self) -> str:
        return f"<Broker id={self.id}, company={self.company_name}>"
