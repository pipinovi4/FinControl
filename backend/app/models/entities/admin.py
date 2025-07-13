from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, ForeignKey, Boolean
from backend.app.models.entities import User
from backend.app.models.mixins import TimeStampAuthMixin, DynamicLinkAuthMixin
from backend.app.permissions import PermissionRole


class Admin(User, TimeStampAuthMixin, DynamicLinkAuthMixin):
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
        nullable=False,
        unique=True,
        info={"description": "Friendly name for the admin (used in dashboards/logs)"}
    )

    is_super_admin: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        info={"description": "Whether the admin is super admin"}
    )

    __mapper_args__ = {
        "inherit_condition": (id == User.id),
        "polymorphic_identity": PermissionRole.ADMIN,
    }

    def __repr__(self) -> str:
        return f"<Admin id={self.id}, name={self.display_name}>"
