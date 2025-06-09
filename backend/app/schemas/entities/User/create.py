from backend.app.permissions import PermissionRole
from backend.app.schemas.entities.User import UserBase

class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Excludes UUID and timestamps — those are auto-generated.
    """
    telegram_id: str
    telegram_username: str
    role: PermissionRole
    is_active: bool
