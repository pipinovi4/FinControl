from sqlalchemy.orm import Query
from datetime import datetime
from backend.app.models import Admin
from backend.app.permissions import PermissionRole
from backend.app.services.entities import UserFilterService


class AdminFilterService(UserFilterService):
    """
    Service for filtering Admin queries based on dynamic conditions.
    """

    def __init__(self, base_query: Query):
        """Initialize the filter service with a base query."""
        super().__init__(base_query)
        self.query = base_query

    def by_email(self, email: str):
        """Filter admins by email substring (case-insensitive)."""
        self.query = self.query.filter(Admin.email.ilike(f"%{email}%"))
        return self

    def by_display_name(self, name: str):
        """Filter admins by display name substring (case-insensitive)."""
        self.query = self.query.filter(Admin.display_name.ilike(f"%{name}%"))
        return self

    def by_role(self, role: PermissionRole):
        """Filter admins by exact role."""
        self.query = self.query.filter(Admin.role == role)
        return self

    def by_is_active(self, is_active: bool = True):
        """Filter admins by active status."""
        self.query = self.query.filter(Admin.is_active == is_active)
        return self

    def by_is_deleted(self, is_deleted: bool = False):
        """Filter admins by deletion status."""
        self.query = self.query.filter(Admin.is_deleted == is_deleted)
        return self

    def by_created_after(self, dt: datetime):
        """Filter admins created after a specific datetime."""
        self.query = self.query.filter(Admin.created_at >= dt)
        return self

    def by_created_before(self, dt: datetime):
        """Filter admins created before a specific datetime."""
        self.query = self.query.filter(Admin.created_at <= dt)
        return self

    def exclude_superadmins(self):
        """Exclude admins with SUPERADMIN role."""
        self.query = self.query.filter(Admin.is_super_admin == False)
        return self

    def search_email_or_display_name(self, text: str):
        """Search admins by email or display name substring."""
        like = f"%{text}%"
        self.query = self.query.filter(
            (Admin.email.ilike(like)) | (Admin.display_name.ilike(like))
        )
        return self

    def apply(self):
        """Finalize and return the filtered query."""
        return self.query
