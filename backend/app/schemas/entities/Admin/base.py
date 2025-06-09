from typing import Optional
from pydantic import Field
from backend.app.schemas.entities import UserSchema
from backend.app.schemas.mixins import (
    AuthSchema,
    TimeStampAuthSchema,
    DynamicLinkAuthSchema
)

class AdminBase(
    UserSchema.Base,
    AuthSchema,
    TimeStampAuthSchema,
    DynamicLinkAuthSchema
):
    """
    Shared schema for the Admin entity.

    Inherits:
      - UserSchema.Base           (id, timestamps, full_name, telegram info)
      - AuthSchema                (email, password_hash [excluded on output])
      - TimeStampAuthSchema       (last_login_at)
      - DynamicLinkAuthSchema     (dynamic_login_token)

    Adds:
      - display_name              (optional friendly name for UI/logs)
    """
    display_name: Optional[str] = Field(
        None,
        example="Jane Admin",
        description="Friendly display name used in dashboards or logs"
    )
