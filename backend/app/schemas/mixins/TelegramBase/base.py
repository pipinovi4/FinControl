from pydantic import Field
from backend.app.schemas import SchemaBase


class TelegramSchema(SchemaBase):
    """
    Schema representing Telegram user information.

    Used as a mixin/base for user-related models that include Telegram integration.

    Fields:
    - telegram_id: Unique identifier for the Telegram user (as string).
    - telegram_username: Optional Telegram username/display name.
    """

    telegram_id: str = Field(..., example="123456789")
    telegram_username: str = Field(..., example="pipin")
