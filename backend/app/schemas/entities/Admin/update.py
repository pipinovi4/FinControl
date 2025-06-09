from typing import Optional
from pydantic import Field, EmailStr

from backend.app.schemas.entities import UserSchema

class AdminUpdate(UserSchema.Update):
    """
    Schema for updating an existing Admin.

    Inherits all optional user-update fields, then adds:
      - display_name
    """
    display_name: Optional[str] = Field(
        None,
        example="Jane A.",
        description="Updated friendly display name"
    )
