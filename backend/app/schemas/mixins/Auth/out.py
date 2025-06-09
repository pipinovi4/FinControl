from pydantic import BaseModel, EmailStr, Field

class AuthOut(BaseModel):
    """
    Public-facing schema for authentication info in API responses.

    Only exposes the user’s email; no password or hash.
    """
    email: EmailStr = Field(..., example="user@example.com")
