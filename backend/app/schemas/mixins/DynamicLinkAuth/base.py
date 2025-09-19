from typing import Optional
from pydantic import Field

class DynamicLinkAuthSchema:
    """
    Base schema for dynamic login authentication.

    This schema includes the dynamic token that can be used for secure,
    time-limited, passwordless login. Typically sent via Telegram or email.
    """

    dynamic_login_token: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Optional login token used for secure dynamic link authentication."
    )
