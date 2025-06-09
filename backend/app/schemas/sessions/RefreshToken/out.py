# Output schema for exposing RefreshToken data in API responses
from datetime import datetime
from uuid import UUID
from .base import RefreshTokenBase

class RefreshTokenOut(RefreshTokenBase):
    id: UUID
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True  # Enables ORM-style conversion from SQLAlchemy models
