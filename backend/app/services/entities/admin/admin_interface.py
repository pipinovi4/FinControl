"""
AdminInterfaceService — generic wrapper around the Admin model.

This class wraps an Admin entity, providing convenient access to
its properties through a unified interface. Useful for rendering views,
performing role checks, and reducing logic duplication in routes/services.

TypeVars:
    AdminT — any entity subclassing Admin.

Includes:
    - is_super_admin(): Check if the admin is a SUPERADMIN.
    - get_display_name(): Return the admin’s display name or a fallback.
    - get_email(): Return the admin’s email.
    - is_active(): Check if the admin is active (not soft-deleted).
    - get_last_login(): Return last login timestamp or 'N/A'.
    - __str__(): Developer-friendly string for debugging.
"""

from backend.app.models import Admin
from backend.app.services.entities import UserInterfaceService
from typing import TypeVar

AdminT = TypeVar("AdminT", bound=Admin)


class AdminInterfaceService(UserInterfaceService):
    def __init__(self, admin: AdminT):
        """Initialize with an Admin instance."""
        super().__init__(admin)
        self.admin: AdminT = admin

    def is_super_admin(self) -> bool:
        """Return True if the admin is a SUPERADMIN."""
        return getattr(self.admin, "is_super_admin", False)

    def get_display_name(self) -> str:
        """Return display name or fallback."""
        return self.admin.display_name or f"Admin#{str(self.admin.id)[:6]}"

    def get_email(self) -> str:
        """Return admin's email."""
        return str(self.admin.email)

    def is_active(self) -> bool:
        """Return True if the admin is not soft-deleted."""
        return not self.admin.is_deleted

    def get_last_login(self) -> str:
        """Return last login time as string or 'N/A'."""
        return str(self.admin.last_login_at) if getattr(self.admin, "last_login", None) else "N/A"

    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Admin(display_name={self.admin.display_name}, id={self.admin.id})"
