from typing import Optional
from pydantic import EmailStr, Field

class AuthUpdate:
    """
    Schema for updating authentication credentials.

    Allows a user to change their email and/or password.
    At least one field should be provided.
    """
    email: Optional[EmailStr] = Field(
        None,
        example="new.user@example.com",
        description="New email address for the user"
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        example="NewStr0ngP@ss",
        description="New plain-text password (will be hashed server-side)"
    )