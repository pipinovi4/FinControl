from datetime import datetime
from pydantic import BaseModel, Field


class TimeStampSchema(BaseModel):
    """
    Schema for timestamp tracking fields.

    Includes:
    - created_at: The datetime when the record was created.
    - updated_at: The datetime when the record was last updated.

    These fields are useful for displaying and debugging data lifecycle.
    """

    created_at: datetime = Field(..., description="UTC timestamp when the record was created.")
    updated_at: datetime = Field(..., description="UTC timestamp when the record was last updated.")
