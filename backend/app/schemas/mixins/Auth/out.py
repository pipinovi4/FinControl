from pydantic import EmailStr, Field

class AuthOut:
    """
    Public-facing schema for authentication info in API responses.

    Only exposes the user’s email; no password or hash.
    """
    email: EmailStr = Field(..., example="user@example.com")
