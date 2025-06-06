import uuid
from pydantic import BaseModel, ConfigDict, Field

class UUIDSchema(BaseModel):
    """
    Shared schema for models using UUID as a primary key.
    Intended for output only — UUID is auto-generated.
    """

    id: uuid.UUID = Field(..., description="Universally unique identifier (UUID v4)")

    model_config = ConfigDict(from_attributes=True)
