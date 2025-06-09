from pydantic import BaseModel, EmailStr, Field

class AuthCreate(BaseModel):
    """
    Schema for user sign-up / login via email + plain-text password.

    Accepts:
    - email: user identifier
    - password: plain-text password (min length enforced)
    """
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., min_length=8, example="strongP@ssw0rd", description="User’s plain-text password")
