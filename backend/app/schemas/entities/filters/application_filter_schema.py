# backend/app/schemas/entities/filters/application_filter_schema.py

from pydantic import Field

from app.schemas.entities.application_schema import ApplicationBase

class ApplicationFilterSchema(ApplicationBase):
    """
    Filter schema for querying Application entities.

    Includes:
        - Basic application fields (id, telegram_id, data, timestamps)
        - User filter fields (date from/to, search text etc.)

    Excludes:
        - Worker object
        - Broker object
        - Credits list
        - Server-only fields, if added later
    """

    worker: None = Field(exclude=True)
    broker: None = Field(exclude=True)
    credits: None = Field(exclude=True)
