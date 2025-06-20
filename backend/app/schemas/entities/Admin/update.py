from pydantic import Field

from backend.app.schemas.entities.User import UserSchema

class AdminUpdate(UserSchema.Update):
    """
    Schema for updating an existing Admin.

    Inherits all optional user-update fields, then adds:
      - display_name
    """
    display_name: str = Field(
        ...,
        example="Jane A.",
        description="Updated friendly display name"
    )
