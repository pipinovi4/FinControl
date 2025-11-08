from typing import TypeVar
from app.models.entities import Admin

AdminT = TypeVar("AdminT", bound=Admin)


class AdminUtilService:
    """
    AdminUtils — helper class for Admin-related logic.

    This class provides static utility methods for use in services or routes.

    Methods:
        is_super_admin(admin): Check if the admin has SUPERADMIN role.
        can_edit_other_admins(admin): Check if the admin can modify other admins.
        sanitize_admin_payload(data): Remove restricted fields from input.
    """
    @staticmethod
    def is_super_admin(admin: AdminT) -> bool:
        """Check if the admin has SUPERADMIN role."""
        return bool(getattr(admin, "is_super_admin", False))

    @staticmethod
    def can_edit_other_admins(admin: AdminT) -> bool:
        """Allow only superadmins to edit or delete other admins."""
        return AdminUtilService.is_super_admin(admin)

    @staticmethod
    def sanitize_admin_payload(data: dict) -> dict:
        """
        Remove restricted fields from incoming payload.
        Prevent creation of superadmins or role changes through insecure endpoints.
        """
        return {
            key: value for key, value in data.items()
            if key not in {"role", "is_superuser", "is_staff"}
        }
