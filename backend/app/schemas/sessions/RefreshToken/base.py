# Base schema for RefreshToken containing shared fields
# used in multiple schema variations (e.g. output)
from pydantic import BaseModel
from uuid import UUID

class RefreshTokenBase(BaseModel):
    user_id: UUID
    user_agent: str
    ip_address: str
    fingerprint: str
