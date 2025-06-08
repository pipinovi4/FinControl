from pydantic import BaseModel
from backend.app.permissions import PermissionRole

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Excludes UUID and timestamps — those are auto-generated.
    """
    telegram_id: str
    telegram_username: str
    role: PermissionRole
    is_active: bool
