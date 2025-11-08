from sqlalchemy import select
from sqlalchemy.sql import Select
from datetime import datetime
from app.models import Admin
from app.permissions import PermissionRole
from app.services.entities import UserFilterService


class AdminFilterService(UserFilterService):
    """
    AdminFilterService builds async-compatible SELECT queries for filtering Admins.

    Inherits:
        UserFilterService – Provides shared filter logic.

    Public Methods:
        - by_email(email): Filter admins by partial email match (ILIKE).
        - by_display_name(name): Filter by partial display name.
        - by_role(role): Filter admins by exact role.
        - by_is_active(is_active): Filter by active status (True/False).
        - by_is_deleted(is_deleted): Filter by deletion status.
        - by_created_after(dt): Filter admins created after given datetime.
        - by_created_before(dt): Filter admins created before given datetime.
        - exclude_superadmins(): Exclude users with is_super_admin=True.
        - search_email_or_display_name(text): Search by partial match in email or display name.
        - apply(): Finalize and return the composed SQLAlchemy Select query.
    """
    def __init__(self):
        """Initialize the filter service with a base SELECT query."""
        super().__init__()
        self.query: Select = select(Admin)

    def by_email(self, email: str):
        """
        Filter admins by email substring (case-insensitive).

        :param email: Substring of the email to search for.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.email.ilike(f"%{email}%"))
        return self

    def by_display_name(self, name: str):
        """
        Filter admins by display name substring (case-insensitive).

        :param name: Substring of the display name to search for.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.display_name.ilike(f"%{name}%"))
        return self

    def by_role(self, role: PermissionRole):
        """
        Filter admins by exact role.

        :param role: PermissionRole enum value.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.role == role)
        return self

    def by_is_active(self, is_active: bool = True):
        """
        Filter admins by active status.

        :param is_active: Boolean indicating if the admin is active.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.is_active == is_active)
        return self

    def by_is_deleted(self, is_deleted: bool = False):
        """
        Filter admins by deletion status.

        :param is_deleted: Boolean indicating if the admin is marked as deleted.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.is_deleted == is_deleted)
        return self

    def by_created_after(self, dt: datetime):
        """
        Filter admins created after a specific datetime.

        :param dt: Datetime value to filter by.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.created_at >= dt)
        return self

    def by_created_before(self, dt: datetime):
        """
        Filter admins created before a specific datetime.

        :param dt: Datetime value to filter by.
        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.created_at <= dt)
        return self

    def exclude_superadmins(self):
        """
        Exclude admins with SUPERADMIN role.

        :return: Self (chainable).
        """
        self.query = self.query.where(Admin.is_super_admin == False)
        return self

    def search_email_or_display_name(self, text: str):
        """
        Search admins by email or display name substring.

        :param text: Text to search for in email or display name.
        :return: Self (chainable).
        """
        like = f"%{text}%"
        self.query = self.query.where(
            (Admin.email.ilike(like)) | (Admin.display_name.ilike(like))
        )
        return self

    def apply(self) -> Select:
        """
        Finalize and return the built SQLAlchemy Select query.

        :return: A Select statement ready for async execution.
        """
        return self.query
