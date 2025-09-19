from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterRequest(BaseModel):
    """
    Schema for user registration.

    Attributes:
        email (EmailStr): User's email address. Must be a valid email format.
        username (str): Unique username, 3–32 characters.
        password (str): Password with a minimum length of 8 characters.
    """
    email: EmailStr = Field(..., description="Valid user email address")
    username: str = Field(..., min_length=3, max_length=32, description="Username (3–32 characters)")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
