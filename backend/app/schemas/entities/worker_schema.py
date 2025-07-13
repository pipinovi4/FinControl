from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

from backend.app.permissions import PermissionRole
from backend.app.schemas.entities.user_schema import UserSchema

if TYPE_CHECKING:
    from backend.app.schemas.entities.client_schema import ClientShort # noqa 401
    from backend.app.schemas.entities.earning_schema import EarningShort # noqa 401


# ───────────── BASE ─────────────
class WorkerBase(UserSchema.Base):
    username: str = Field(..., description="Унікальний внутрішній логін")


# ───────────── CREATE ─────────────
class WorkerCreate(UserSchema.Create):
    username: str = Field(..., description="Унікальний внутрішній логін")


# ───────────── UPDATE ─────────────
class WorkerUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Нове значення логіну")
    telegram_username: Optional[str] = Field(None, description="Нове значення telegram @username")


# ───────────── OUT (API full view) ─────────────
class WorkerOut(WorkerBase):
    clients: Optional[List["ClientShort"]] = Field(default_factory=list)
    earnings: Optional[List["EarningShort"]] = Field(default_factory=list)
    role: PermissionRole = Field(..., description="Роль користувача")


# ───────────── WEB REGISTER RESPONSE ─────────────
class WorkerWebRegisterResponse(UserSchema.Base):
    id: UUID
    email: EmailStr
    username: Optional[str]
    earnings: Optional[List["EarningShort"]] = Field(default_factory=list)


# ───────────── SHORT ─────────────
class WorkerShort(BaseModel):
    id: UUID
    username: str
    email: EmailStr


# ───────────── WRAPPER ─────────────
class WorkerSchema:
    Base = WorkerBase
    Create = WorkerCreate
    Update = WorkerUpdate
    Out = WorkerOut
    Short = WorkerShort
    WebRegisterResponse = WorkerWebRegisterResponse


from importlib import import_module

_worker_mod = import_module("backend.app.schemas.entities.client_schema")
globals()["ClientShort"] = _worker_mod.ClientSchema.Short
_worker_mod = import_module("backend.app.schemas.entities.earning_schema")
globals()["EarningShort"] = _worker_mod.EarningSchema.Short
