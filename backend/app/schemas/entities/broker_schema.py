# backend/app/schemas/entities/broker_schema.py
from __future__ import annotations

from typing import Optional, List, Type, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

from app.permissions import PermissionRole
from app.schemas import SchemaBase
from app.schemas.entities.user_schema import UserSchema
from uuid import UUID

if TYPE_CHECKING:
    from app.schemas.entities.client_schema import ClientShort # noqa 401
    from app.schemas.entities.credit_schema import CreditShort # noqa 401

class BrokerBase(UserSchema.Base):
    """
    Shared schema for the Broker entity.
    """
    company_name: Optional[str] = Field(None, example="Acme Ltd.", description="Broker's company name")
    region: Optional[List[str]] = Field(None, example=["Kyiv", "Lviv"], description="Regions of operation")


class BrokerCreate(UserSchema.Create):
    """
    Schema for creating a Broker.
    """
    company_name: Optional[str] = Field(None, example="Acme Ltd.")
    region: Optional[List[str]] = Field(None, example=["Kyiv", "Lviv"])


class BrokerUpdate(SchemaBase):
    """
    Schema for updating a Broker.
    """
    company_name: Optional[str] = Field(None, example="New Name Ltd.")
    region: Optional[List[str]] = Field(None, example=["Dnipro", "Odessa"])
    email: Optional[EmailStr] = None


class BrokerOut(SchemaBase):
    """
    Schema for returning Broker data with related clients.
    """
    clients: Optional[List["ClientShort"]] = Field(None, description="List of clients assigned to this broker")
    role: PermissionRole = Field(..., description="User role")
    credits: Optional[List["CreditShort"]] = Field(
        None, description="List of client's credit records"
    )
    company_name: Optional[str] = Field(None, example="Acme Ltd.", description="Broker's company name")
    region: Optional[List[str]] = Field(None, example=["Kyiv", "Lviv"], description="Regions of operation")
    is_deleted: bool = False


class BrokerWebRegisterResponse(UserSchema.Base):
    """
    Schema returned after successful broker registration via web.
    """
    id: UUID = Field(..., description="Unique broker ID")
    email: EmailStr = Field(..., description="Email used for login")
    company_name: Optional[str] = Field(None, description="Name of the broker's company")
    region: Optional[List[str]] = Field(None, description="List of regions where the broker is active")
    credits: Optional[List["CreditShort"]] = Field(
        None, description="List of client's credit records"
    )
    clients: Optional[List["ClientShort"]] = Field(None, description="List of clients assigned to this broker")
    is_deleted: bool = False


class BrokerShort(SchemaBase):
    id: UUID
    email: EmailStr
    company_name: Optional[str] = None
    region: Optional[List[str]] = Field(None, description="List of regions where the broker is active")
    is_deleted: bool = False

class BrokerAdminOut(SchemaBase):
    """
    Schema for a Client as seen by a Broker — includes worker info.
    """
    id: UUID
    email: EmailStr
    company_name: Optional[str] = None
    region: Optional[List[str]] = Field(None, description="List of regions where the broker is active")
    created_at: datetime
    is_deleted: bool = False


class BrokerSchema:
    Base:   Type[BaseModel] = BrokerBase
    Create: Type[BaseModel] = BrokerCreate
    Update: Type[BaseModel] = BrokerUpdate
    Out:    Type[BaseModel] = BrokerOut
    Short:  Type[BaseModel] = BrokerShort
    WebRegisterResponse: Type[BaseModel] = BrokerWebRegisterResponse

from importlib import import_module

_broker_mod = import_module("app.schemas.entities.client_schema")
globals()["ClientShort"] = _broker_mod.ClientSchema.Short
_broker_mod = import_module("app.schemas.entities.credit_schema")
globals()["CreditShort"] = _broker_mod.CreditSchema.Short
