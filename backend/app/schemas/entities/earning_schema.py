from uuid import UUID
from pydantic import Field
from typing import Optional, TYPE_CHECKING
import datetime

from backend.app.schemas import SchemaBase

if TYPE_CHECKING:
    from backend.app.schemas.entities.client_schema import ClientShort # noqa 401
    from backend.app.schemas.entities.earning_schema import EarningShort # noqa 401


# ──────────────── BASE ────────────────
class EarningBase(SchemaBase):
    date: datetime.date = Field(..., description="Дата нарахування")
    amount: float = Field(..., description="Сума винагороди (в грн, доларах або ін. валюті)")


# ─────────────── CREATE ───────────────
class EarningCreate(SchemaBase):
    worker_id: UUID
    client_id: UUID
    amount: float
    date: datetime.date

class EarningCreateIn(SchemaBase):
    worker_id: UUID
    client_id: UUID
    amount: float

# ─────────────── UPDATE ───────────────
class EarningUpdate(SchemaBase):
    amount: Optional[float] = None
    client_id: Optional[UUID] = None
    worker_id: Optional[UUID] = None


# ─────────────── OUT ───────────────
class EarningOut(EarningBase):
    id: UUID
    worker_id: UUID
    client_id: UUID
    amount: float
    date: datetime.date
    worker: Optional["WorkerShort"]


# ─────────────── SHORT ───────────────
class EarningShort(EarningOut):
    pass


# ─────────────── WRAPPER ───────────────
class EarningSchema:
    Base = EarningBase
    Create = EarningCreate
    Update = EarningUpdate
    Out = EarningOut
    Short = EarningShort

from importlib import import_module

_earning_mod = import_module("backend.app.schemas.entities.worker_schema")
globals()["WorkerShort"] = _earning_mod.WorkerSchema.Short
_earning_mod = import_module("backend.app.schemas.entities.client_schema")
globals()["ClientShort"] = _earning_mod.ClientSchema.Short
