from pydantic import BaseModel, EmailStr, Field

class WorkerCreate(BaseModel):
    """
    Schema for creating a new Worker.

    Accepts:
    - email               (user’s login email)
    - password            (plain-text password)
    - full_name           (worker’s displayed name)
    - username            (internal login username)
    - telegram_username   (optional Telegram handle)
    """
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(
        ..., min_length=8, example="StrongP@ssw0rd",
        description="Plain-text password; will be hashed server-side"
    )
    full_name: str = Field(
        ..., example="John Smith",
        description="Worker’s full display name"
    )
    username: str = Field(
        ..., example="john.smith",
        description="Unique internal username for login"
    )
    telegram_username: str | None = Field(
        None, example="pipin",
        description="Optional Telegram username"
    )
