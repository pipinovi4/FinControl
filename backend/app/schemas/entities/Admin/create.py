from datetime import datetime
from typing import Optional
from pydantic import Field

from backend.app.schemas.mixins import DynamicLinkAuthSchema
from backend.app.schemas.mixins import AuthSchema
from backend.app.schemas.entities.User import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema


class AdminCreate(UserSchema.Create, AuthSchema.Create, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Schema for creating a new Admin.

    Inherits:
      - UserSchema.Create  (email, telegram_id, telegram_username, is_active)
    Adds:
      - display_name, is_super_admin, password_hash, etc.
    """

    display_name: str = Field(
        default="Unnamed Admin",
        example="Jane Admin",
        description="Friendly display name for dashboard or logs"
    )

    is_super_admin: bool = Field(
        default=False,
        description="If true, grants full root access to admin features"
    )

