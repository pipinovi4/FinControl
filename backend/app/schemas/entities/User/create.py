from backend.app.permissions.enums import PermissionRole
from backend.app.schemas import SchemaBase


class UserCreate(SchemaBase):
    """
    Schema for creating a new user.

    Excludes UUID and timestamps — those are auto-generated.
    """
    telegram_id: str
    telegram_username: str
    role: PermissionRole
    is_active: bool
