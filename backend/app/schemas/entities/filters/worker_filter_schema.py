# backend/app/schemas/filters/worker_filter_schema.py

from typing import Optional
from pydantic import Field

from app.schemas import WorkerSchema
from app.schemas.entities.filters import UserFilterSchema


class WorkerFilterSchema(WorkerSchema.Base, UserFilterSchema):
    """
    Filter schema for querying Worker entities.

    Supports:
    - filtering by username or telegram handle
    - filtering by activity or role presence if needed
    """
    username: Optional[str] = Field(
        None,
        example="john.smith",
        description="Filter workers by internal username"
    )
    email: Optional[str] = Field(
        None,
        example="worker@example.com",
        description="Filter by email (partial match supported)"
    )
    full_name: Optional[str] = Field(
        None,
        example="John Smith",
        description="Filter by full name"
    )
