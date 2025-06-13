# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access expires
