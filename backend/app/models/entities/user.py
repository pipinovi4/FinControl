from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String

from backend.app.models.mixins import UUIDMixin, TimeStampMixin, SoftDeleteMixin, AuthMixin
from backend.app.permissions.enums import PermissionRole
from backend.db.session import Base

class User(Base, AuthMixin, UUIDMixin, TimeStampMixin, SoftDeleteMixin):
    """
    Base user model used as a parent class for all user roles:
    Client, Worker, Broker, and Admin.

    Inherits:
    - UUIDMixin: provides UUID primary key as 'id'
    - TimeStampMixin: provides 'created_at' and 'updated_at' fields

    This class serves as a polymorphic base for role-based subclasses.
    """

    __tablename__ = 'users'

    telegram_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    # Telegram internal ID used as external identifier for bots

    telegram_username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    # Username of the user in Telegram, used for display/logging/search

    role: Mapped[PermissionRole] = mapped_column(
        Enum(PermissionRole),
        nullable=False
    )
    # Enum-based user role: defines access level and behavior (e.g., client, admin)

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )
    # Logical flag indicating if the user is allowed to access the system

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "user",
    }

    def __repr__(self):
        """
        Developer-friendly string representation for debugging/logging purposes.
        """
        return f"<User - {self.telegram_username}: ({self.role.value}). ID: {self.telegram_id} is {self.is_active}>"
