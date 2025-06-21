# backend/app/schemas/entities/filters/client_filter_schema.py

from backend.app.schemas.entities.client_schema import ClientSchema
from pydantic import Field


class ClientFilterSchema(ClientSchema.Base):
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
