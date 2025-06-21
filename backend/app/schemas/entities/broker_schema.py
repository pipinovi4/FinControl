# backend/app/schemas/entities/broker_schema.py
from __future__ import annotations

from typing import Optional, List, Type, ForwardRef
from pydantic import BaseModel, Field

from backend.app.schemas.entities.user_schema import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema

# To avoid circular import with ClientSchema
ClientOut = ForwardRef("ClientSchema.Out")


class BrokerBase(UserSchema.Base):
    """
    Shared schema for the Broker entity.
    """
    company_name: Optional[str] = Field(None, example="Acme Ltd.", description="Broker's company name")
    region: Optional[List[str]] = Field(None, example=["Kyiv", "Lviv"], description="Regions of operation")


class BrokerCreate(UserSchema.Create, TimeStampAuthSchema):
    """
    Schema for creating a Broker.
    """
    company_name: Optional[str] = Field(None, example="Acme Ltd.")
    region: Optional[List[str]] = Field(None, example=["Kyiv", "Lviv"])


class BrokerUpdate(BaseModel):
    """
    Schema for updating a Broker.
    """
    company_name: Optional[str] = Field(None, example="New Name Ltd.")
    region: Optional[List[str]] = Field(None, example=["Dnipro", "Odessa"])
    telegram_username: Optional[str] = Field(None, example="newbroker")


class BrokerOut(BrokerBase, TimeStampAuthSchema):
    """
    Schema for returning Broker data with related clients.
    """
    clients: Optional[List["ClientSchema.Out"]] = Field(None, description="List of clients assigned to this broker")


class BrokerSchema:
    Base:   Type[BaseModel] = BrokerBase
    Create: Type[BaseModel] = BrokerCreate
    Update: Type[BaseModel] = BrokerUpdate
    Out:    Type[BaseModel] = BrokerOut
