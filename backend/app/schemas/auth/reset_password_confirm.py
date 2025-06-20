from pydantic import BaseModel, Field, field_validator


class ResetPasswordConfirm(BaseModel):
    """
    Schema for confirming password reset.

    Fields:
        token (str): The JWT reset token received via email.
        new_password (str): The new password to be set.
                            Must be at least 8 characters.
    """
    token: str
    new_password: str = Field(..., description="New password (min. 8 characters)")

    @field_validator("new_password")
    def validate_password(self, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if len(v) > 32:
            raise ValueError("Password must be at most 32 characters long")

        return v
