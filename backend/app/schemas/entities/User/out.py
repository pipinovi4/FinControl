from backend.app.schemas.entities.User import UserBase
from backend.app.schemas.mixins import UUIDSchema, TimeStampSchema

class UserOut(UserBase, UUIDSchema, TimeStampSchema):
    """
    Schema for returning user data to clients.

    Combines:
    - Basic user info (telegram ID, username, role, status)
    - Metadata (UUID, created_at, updated_at)
    """
    pass
