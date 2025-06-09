# Output schema for exposing RefreshToken data in API responses
from datetime import datetime
from uuid import UUID
from .base import RefreshTokenBase

# TODO need to add UUIDMixinSchema and TimeStampMixinSchema when it bee ready instead hand wrote id, created_at, update_at

class RefreshTokenOut(RefreshTokenBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    expires_at: datetime
