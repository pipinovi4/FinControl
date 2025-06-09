from pydantic import Field
from backend.app.schemas.entities import UserSchema
from backend.app.schemas.mixins import (
    AuthSchema,
    TimeStampAuthSchema,
    DynamicLinkAuthSchema
)


class WorkerBase(
    UserSchema.Base,
    AuthSchema,
    TimeStampAuthSchema,
    DynamicLinkAuthSchema
):
    """
    Shared schema for the Worker entity.

    Inherits:
      - UserSchema.Base           (id, full_name, telegram info, timestamps)
      - AuthSchema                (email, password_hash)
      - TimeStampAuthSchema       (last_login_at)
      - DynamicLinkAuthSchema     (dynamic_login_token)

    Adds:
      - username                  (internal login username)
      - telegram_username         (optional contact handle)
    """
    username: str = Field(
        ..., example="john.smith",
        description="Internal login username for this worker"
    )
    telegram_username: str | None = Field(
        None, example="pipin",
        description="Optional Telegram username for contacting this worker"
    )
