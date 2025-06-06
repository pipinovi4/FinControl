# Temporary template, in the next 10 hours of work I will change it to JWT Auth


from pydantic import BaseModel, EmailStr, Field

class AuthSchema(BaseModel):
    """
    AuthSchema:
    Base Pydantic schema representing authentication fields used in models.

    Includes:
    - email: primary user identity field
    - password_hash: securely stored hashed password (not exposed in public schemas)

    This schema can be used as a base for internal models or validation in secure contexts.
    Avoid exposing `password_hash` in public response schemas.
    """

    email: EmailStr = Field(..., example="user@example.com")
    password_hash: str = Field(..., exclude=True)

    class Config:
        orm_mode = True
