from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, ForeignKey
from backend.app.models import User
from backend.app.models.mixins import AuthMixin, TimeStampAuthMixin, DynamicLinkAuthMixin

class Admin(User, AuthMixin, TimeStampAuthMixin, DynamicLinkAuthMixin):
    """
    Admin model — full-access user with complete control over the system.

    Inherits:
    - User: basic role/Telegram linkage
    - AuthMixin: standard auth via email + password hash
    - TimeStampAuthMixin: login timestamp tracking
    - DynamicLinkAuthMixin: login via time-limited magic links
    """

    __tablename__ = "admins"

    # Primary key linked to base User ID
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Optional display name for UI or logs
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Friendly name for the admin (used in dashboards/logs)"
    )

    __mapper_args__ = {
        "polymorphic_identity": "admin"
    }

    def __repr__(self) -> str:
        return f"<Admin id={self.id}, name={self.display_name}>"
