from __future__ import annotations

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

from backend.app.permissions import PermissionRole
from backend.app.schemas import SchemaBase
from backend.app.schemas.entities.user_schema import UserSchema

if TYPE_CHECKING:
    from backend.app.schemas.entities.client_schema import ClientShort  # noqa: F401
    from backend.app.schemas.entities.credit_schema import CreditShort  # noqa: F401


# ───────────── BASE ─────────────
class WorkerBase(UserSchema.Base):
    username: str = Field(..., description="Унікальний внутрішній логін")


# ───────────── CREATE ─────────────
class WorkerCreate(UserSchema.Create):
    username: str = Field(..., description="Унікальний внутрішній логін")


# ───────────── UPDATE ─────────────
class WorkerUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Нове значення логіну")
    email: Optional[EmailStr] = None


# ───────────── OUT (API full view) ─────────────
class WorkerOut(WorkerBase):
    clients: Optional[List["ClientShort"]] = Field(default_factory=list)
    credits: Optional[List["CreditShort"]] = Field(default_factory=list)
    role: PermissionRole = Field(..., description="Роль користувача")
    is_deleted: bool = False


# ───────────── WEB REGISTER RESPONSE ─────────────
class WorkerWebRegisterResponse(UserSchema.Base):
    id: UUID
    email: EmailStr
    username: Optional[str]
    credits: Optional[List["CreditShort"]] = Field(default_factory=list)
    clients: Optional[List["ClientShort"]] = Field(default_factory=list)
    is_deleted: bool = False


# ───────────── SHORT ─────────────
class WorkerShort(SchemaBase):
    id: UUID
    username: str
    email: EmailStr
    is_deleted: bool = False


class WorkerAdminOut(SchemaBase):
    """
    Schema for a Worker as seen by Admin.
    """
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    is_deleted: bool = False


# ───────────── WRAPPER ─────────────
class WorkerSchema:
    Base = WorkerBase
    Create = WorkerCreate
    Update = WorkerUpdate
    Out = WorkerOut
    Short = WorkerShort
    WebRegisterResponse = WorkerWebRegisterResponse


# resolve forward refs without circular imports at import time
from importlib import import_module

_client_mod = import_module("backend.app.schemas.entities.client_schema")
globals()["ClientShort"] = _client_mod.ClientSchema.Short

_credit_mod = import_module("backend.app.schemas.entities.credit_schema")
globals()["CreditShort"] = _credit_mod.CreditSchema.Short
