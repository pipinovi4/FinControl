from pydantic import Field

from backend.app.schemas.entities.User import UserSchema

class AdminCreate(UserSchema.Create):
    """
    Schema for creating a new Admin.

    Inherits:
      - UserSchema.Create  (email, password, full_name)
    Adds:
      - display_name       (optional friendly name for UI/logs)
    """
    display_name: str = Field(
        ...,
        example="Jane Admin",
        description="Friendly display name for dashboard or logs"
    )
