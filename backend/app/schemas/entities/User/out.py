from backend.app.schemas.mixins import AuthSchema
from backend.app.schemas.entities.User.base import UserBase

class UserOut(UserBase, AuthSchema.Out):
    """
    Schema for returning user data to clients.

    Combines:
    - Basic user info (telegram ID, username, role, status)
    - Metadata (UUID, created_at, updated_at)
    """
    pass
