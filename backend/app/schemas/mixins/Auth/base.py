from pydantic import EmailStr, Field

class AuthBase:
    """
    Internal schema for authentication models.

    Holds the securely stored password hash alongside user identity.
    Not exposed in public API responses.
    """
    email: EmailStr = Field(..., example="user@example.com")
    password_hash: str = Field(..., exclude=True, description="Hashed user password; never exposed")