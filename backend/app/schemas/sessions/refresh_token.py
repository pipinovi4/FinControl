# backend/app/schemas/entities/RefreshToken.py

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from backend.app.schemas.mixins import UUIDSchema


class RefreshTokenSchema:
    """
    Container for Pydantic models related to RefreshToken entity.
    Includes schemas for creation and response output.
    """

    class Base(BaseModel):
        """
        Shared base schema for RefreshToken.

        Fields:
            user_id (UUID): Unique identifier of the associated user.
            token_hash (str): Hashed version of the refresh token (SHA-256, 64 characters).
            created_from_ip (Optional[str]): IP address where the token was generated.
            user_agent (Optional[str]): User agent string of the device/session.
            expires_at (datetime): Timestamp when the token expires.
            is_active (bool): Indicates if the token is still valid and active.
        """
        user_id: UUID
        token_hash: Annotated[
            str,
            Field(..., min_length=64, max_length=64, description="SHA-256 hash of the token")
        ]
        created_from_ip: Optional[str] = None
        user_agent: Optional[str] = None
        expires_at: datetime
        is_active: bool = True

        class Config:
            orm_mode = True  # Enable compatibility with ORM models (e.g. SQLAlchemy)

    class Create(Base):
        """
        Schema used when creating a new refresh token.
        Inherits all fields from Base.
        """
        pass

    class Out(Base, UUIDSchema):
        """
        Schema used when returning refresh token data from the API.
        Extends Base and includes UUID from UUIDSchema.
        """
        pass
