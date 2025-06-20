from pydantic import BaseModel, EmailStr

class ResetPasswordRequest(BaseModel):
    """
    Schema for requesting a password reset email.

    Fields:
        email (EmailStr): The user's registered email address to which
                          the reset link will be sent.
    """
    email: EmailStr
