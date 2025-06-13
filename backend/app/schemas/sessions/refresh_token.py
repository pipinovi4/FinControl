# backend/app/schemas/entities/RefreshToken.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated, Optional

from backend.app.schemas.mixins import UUIDSchema


class RefreshTokenSchema:
    class Base(BaseModel):
        user_id: UUID
        token_hash: Annotated[
            str,
            Field(..., min_length=64, max_length=64, description="SHA-256 hash of the token")
        ]
        created_from_ip: Optional[str] = None
        user_agent:      Optional[str] = None
        expires_at: datetime
        is_active: bool = True

        class Config:
            orm_mode = True

    class Create(Base):
        pass

    class Out(Base, UUIDSchema):
        pass
