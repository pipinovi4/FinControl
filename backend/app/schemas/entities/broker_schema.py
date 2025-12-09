# backend/app/schemas/entities/broker_schema.py
from __future__ import annotations

from typing import Optional, List, Type
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from uuid import UUID

from app.permissions import PermissionRole
from app.schemas import SchemaBase
from app.schemas.entities.user_schema import UserSchema

# Forward refs (no TYPE_CHECKING needed)
from app.schemas.entities.application_schema import ApplicationShort
from app.schemas.entities.credit_schema import CreditShort


class BrokerBase(UserSchema.Base):
    """
    Shared schema for the Broker entity.
    """
    company_name: Optional[str] = None
    region: Optional[List[str]] = None


class BrokerCreate(UserSchema.Create):
    company_name: Optional[str] = None
    region: Optional[List[str]] = None


class BrokerUpdate(SchemaBase):
    company_name: Optional[str] = None
    region: Optional[List[str]] = None
    email: Optional[EmailStr] = None


class BrokerOut(SchemaBase):
    """
    Public-facing schema for returning Broker data (full view).
    """
    applications: Optional[List[ApplicationShort]] = Field(default_factory=list)
    credits: Optional[List[CreditShort]] = Field(default_factory=list)
    role: PermissionRole
    company_name: Optional[str] = None
    region: Optional[List[str]] = None
    is_deleted: bool = False


class BrokerWebRegisterResponse(UserSchema.Base):
    """
    Returned after broker is created via web.
    """
    id: UUID
    email: EmailStr
    company_name: Optional[str]
    region: Optional[List[str]]
    applications: Optional[List[ApplicationShort]] = Field(default_factory=list)
    credits: Optional[List[CreditShort]] = Field(default_factory=list)
    is_deleted: bool = False


class BrokerShort(SchemaBase):
    id: UUID
    email: EmailStr
    company_name: Optional[str] = None
    region: Optional[List[str]] = None
    is_deleted: bool = False


class BrokerAdminOut(SchemaBase):
    id: UUID
    email: EmailStr
    company_name: Optional[str]
    region: Optional[List[str]]
    created_at: datetime
    is_deleted: bool = False


class BrokerSchema:
    Base: Type[BaseModel] = BrokerBase
    Create: Type[BaseModel] = BrokerCreate
    Update: Type[BaseModel] = BrokerUpdate
    Out: Type[BaseModel] = BrokerOut
    Short: Type[BaseModel] = BrokerShort
    WebRegisterResponse: Type[BaseModel] = BrokerWebRegisterResponse
