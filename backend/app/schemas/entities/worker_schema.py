from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

from app.permissions import PermissionRole
from app.schemas import SchemaBase
from app.schemas.entities.user_schema import UserSchema

if TYPE_CHECKING:
    from app.schemas.entities.application_schema import ApplicationShort
    from app.schemas.entities.credit_schema import CreditShort


class WorkerBase(UserSchema.Base):
    username: str = Field(..., description="Унікальний внутрішній логін")


class WorkerCreate(UserSchema.Create):
    username: str = Field(..., description="Унікальний внутрішній логін")


class WorkerUpdate(BaseModel):
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = None


class WorkerOut(WorkerBase):
    applications: Optional[List["ApplicationShort"]] = Field(default_factory=list)
    credits: Optional[List["CreditShort"]] = Field(default_factory=list)
    role: PermissionRole = Field(..., description="Роль користувача")
    is_deleted: bool = False


class WorkerWebRegisterResponse(UserSchema.Base):
    id: UUID
    email: EmailStr
    username: Optional[str]
    credits: Optional[List["CreditShort"]] = Field(default_factory=list)
    applications: Optional[List["ApplicationShort"]] = Field(default_factory=list)
    is_deleted: bool = False


class WorkerShort(SchemaBase):
    id: UUID
    username: str
    email: EmailStr
    is_deleted: bool = False


class WorkerAdminOut(SchemaBase):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    is_deleted: bool = False


class WorkerSchema:
    Base = WorkerBase
    Create = WorkerCreate
    Update = WorkerUpdate
    Out = WorkerOut
    Short = WorkerShort
    WebRegisterResponse = WorkerWebRegisterResponse
