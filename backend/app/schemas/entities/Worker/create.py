from pydantic import Field

from backend.app.schemas.mixins import DynamicLinkAuthSchema, TimeStampAuthSchema
from backend.app.schemas.entities import UserSchema


class WorkerCreate(UserSchema.Create, TimeStampAuthSchema, DynamicLinkAuthSchema):
    """
    Schema for creating a new Worker.

    Accepts:
    - email               (user’s login email)
    - password            (plain-text password)
    - full_name           (worker’s displayed name)
    - username            (internal login username)
    - telegram_username   (optional Telegram handle)
    """
    username: str = Field(
        ..., example="john.smith",
        description="Unique internal username for login"
    )
