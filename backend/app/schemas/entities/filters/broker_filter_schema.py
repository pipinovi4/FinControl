# backend/app/schemas/entities/filters/broker_filter_schema.py

from backend.app.schemas.entities.broker_schema import BrokerSchema
from pydantic import Field


class BrokerFilterSchema(BrokerSchema.Base):
    """
    Filter schema for querying Broker entities.

    Inherits all public fields from BrokerSchema.Base
    and explicitly excludes technical/auth-related fields.
    """

    password_hash: None = Field(exclude=True)
    dynamic_login_token: None = Field(exclude=True)
    last_login_at: None = Field(exclude=True)
    created_at: None = Field(exclude=True)
    updated_at: None = Field(exclude=True)
