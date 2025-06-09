from typing import Optional
from pydantic import Field, EmailStr
from uuid import UUID

from backend.app.schemas.entities import UserSchema

class AdminCreate(UserSchema.Create):
    """
    Schema for creating a new Admin.

    Inherits:
      - UserSchema.Create  (email, password, full_name)
    Adds:
      - display_name       (optional friendly name for UI/logs)
    """
    display_name: Optional[str] = Field(
        None,
        example="Jane Admin",
        description="Friendly display name for dashboard or logs"
    )
