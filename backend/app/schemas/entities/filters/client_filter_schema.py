# backend/app/schemas/entities/filters/client_filter_schema.py

from pydantic import Field

from backend.app.schemas.entities.client_schema import ClientSchema
from backend.app.schemas.entities.filters import UserFilterSchema


class ClientFilterSchema(ClientSchema.Base, UserFilterSchema):
    """
    Filter schema for querying Client entities.

    Inherits:
      - All client-visible fields from ClientSchema.Base

    Excludes:
      - Nested Worker and Broker objects
      - Any server-only metadata (if present in future)
    """

    worker: None = Field(exclude=True)
    broker: None = Field(exclude=True)
    report_files: None = Field(exclude=True)
