from pydantic import BaseModel, Field
from backend.app.permissions import PermissionRole

class UserBase(BaseModel):
    """
    Base schema shared across all user-related models.

    Includes:
    - telegram_id: External identifier from Telegram
    - telegram_username: User's Telegram handle
    - role: Role assigned in the system (admin, client, etc.)
    - is_active: Flag indicating whether the user is active
    """
    telegram_id: str = Field(..., example="123456789")
    telegram_username: str = Field(..., example="user")
    role: PermissionRole = Field(..., example=PermissionRole.ADMIN.value)
    is_active: bool = Field(..., example=True)
