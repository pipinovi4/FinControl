from pydantic import BaseModel, Field, field_validator


class ResetPasswordConfirm(BaseModel):
    """
    Schema for confirming password reset.

    Fields:
        token (str): The JWT reset token received via email.
        new_password (str): The new password to be set (8-32 chars).
    """
    token: str
    new_password: str = Field(..., description="New password (8-32 characters)")

    @field_validator("new_password")
    def validate_password(cls, v: str) -> str:      # ← cls, не self
        if not (8 <= len(v) <= 32):
            raise ValueError("Password length must be 8-32 characters")
        return v