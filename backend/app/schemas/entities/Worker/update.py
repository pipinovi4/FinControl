from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class WorkerUpdate(BaseModel):
    """
    Schema for updating Worker profile.

    All fields are optional; only provided ones will be changed.
    """
    email: Optional[EmailStr] = Field(
        None, example="new@example.com",
        description="New login email for the worker"
    )
    password: Optional[str] = Field(
        None, min_length=8, example="NewStr0ngP@ss",
        description="New plain-text password; will be hashed server-side"
    )
    full_name: Optional[str] = Field(
        None, example="John Smith Jr.",
        description="Updated display name"
    )
    username: Optional[str] = Field(
        None, example="john.smith2",
        description="Updated internal username"
    )
    telegram_username: Optional[str] = Field(
        None, example="newpipin",
        description="Updated or cleared Telegram username"
    )
