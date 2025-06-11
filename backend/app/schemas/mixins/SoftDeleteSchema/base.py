from pydantic import Field
from typing import Optional
from datetime import datetime


class SoftDeleteSchema:
    """
    Base schema to support soft deletion logic in API layer.

    Fields:
    - deleted: Logical flag indicating whether the object is considered deleted.
    - deleted_at: Timestamp showing when the object was soft-deleted (if applicable).

    This schema can be reused in any resource that supports soft deletion instead of hard delete.
    """
    deleted: Optional[bool] = Field(
        default=False,
        description="Soft delete flag — True if the object is logically deleted"
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of when the object was soft-deleted"
    )

