# backend/app/schemas/entities/broker_schema.py

from typing import Optional, List, Type
from pydantic import BaseModel, Field

from backend.app.schemas.entities.user_schema import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema


class BrokerBase(UserSchema.Base, TimeStampAuthSchema):
    """
    Shared schema for the Broker entity.
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Name of the broker’s company, if any"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia", "Lesser Poland"],
        description="List of regions where the broker is active"
    )


class BrokerCreate(UserSchema.Create, TimeStampAuthSchema):
    """
    Schema for creating a new Broker.
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Name of the broker’s company"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia", "Lesser Poland"],
        description="Regions where the broker will operate"
    )


class BrokerUpdate(UserSchema.Update):
    """
    Schema for updating an existing Broker.
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Updated company name"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia"],
        description="Updated list of active regions"
    )


class BrokerOut(BrokerBase):
    """
    Public-facing schema for returning Broker data.
    """
    pass


class BrokerSchema:
    Base:   Type[BaseModel] = BrokerBase
    Create: Type[BaseModel] = BrokerCreate
    Update: Type[BaseModel] = BrokerUpdate
    Out:    Type[BaseModel] = BrokerOut
