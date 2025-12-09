# backend/app/schemas/entities/application_schema.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict
from uuid import UUID

from pydantic import Field
from app.schemas import SchemaBase
from app.models.entities.application import ApplicationStatus  # якщо треба


# ─────────────────────────────
# БАЗОВА ЧАСТИНА
# ─────────────────────────────

class ApplicationBase(SchemaBase):
    id: UUID
    telegram_id: int

    worker_id: Optional[UUID] = None
    broker_id: Optional[UUID] = None

    taken_at_worker: Optional[datetime] = None
    taken_at_broker: Optional[datetime] = None

    data: Dict[str, str] = Field(..., description="Canonical wizard answers")


class ApplicationCreate(SchemaBase):
    telegram_id: int
    data: Dict[str, str]


class ApplicationUpdate(SchemaBase):
    data: Optional[Dict[str, str]] = None
    worker_id: Optional[UUID] = None
    broker_id: Optional[UUID] = None
    taken_at_worker: Optional[datetime] = None
    taken_at_broker: Optional[datetime] = None


# ─────────────────────────────
# ВИВОДИ ДЛЯ КОЖНОЇ РОЛІ
# ─────────────────────────────

class ApplicationOut(ApplicationBase):
    credits: Optional[List["CreditShort"]] = []


class ApplicationShort(SchemaBase):
    id: UUID
    full_name: str
    phone_number: str
    email: str


class WorkerApplicationNewToday(SchemaBase):
    id: UUID
    taken_at_worker: datetime


class BrokerApplicationNewToday(SchemaBase):
    id: UUID
    taken_at_broker: datetime


class ApplicationWorkerOut(SchemaBase):
    id: UUID
    data: Dict[str, str]
    taken_at_worker: Optional[datetime] = None
    is_deleted: bool = False


class ApplicationBrokerOut(SchemaBase):
    id: UUID
    data: Dict[str, str]
    taken_at_broker: Optional[datetime] = None
    is_deleted: bool = False


class ApplicationAdminOut(SchemaBase):
    id: UUID
    telegram_id: int
    data: Dict[str, str]
    taken_at_worker: Optional[datetime] = None
    taken_at_broker: Optional[datetime] = None
    created_at: datetime
    is_deleted: bool = False


# ─────────────────────────────
# ПАГІНАЦІЯ
# ─────────────────────────────

class AdminPaginatedApplicationsOut(SchemaBase):
    applications: List[ApplicationAdminOut]
    total: int


class WorkerPaginatedApplicationsOut(SchemaBase):
    applications: List[ApplicationWorkerOut]
    total: int


class BrokerPaginatedApplicationsOut(SchemaBase):
    applications: List[ApplicationBrokerOut]
    total: int


# ─────────────────────────────
# КОРОТКА КРЕДИТ-МОДЕЛЬ (імпорт для типізації)
# ─────────────────────────────
class CreditShort(SchemaBase):
    id: UUID
    amount: float
    status: str
    issued_at: datetime


# ─────────────────────────────
# WRAPPER (ОДИН ВХІД ДЛЯ ВСІХ СХЕМ)
# ─────────────────────────────

class ApplicationSchema:
    Base = ApplicationBase
    Create = ApplicationCreate
    Update = ApplicationUpdate
    Out = ApplicationOut
    Short = ApplicationShort
    WorkerNewToday = WorkerApplicationNewToday
    BrokerNewToday = BrokerApplicationNewToday
    WorkerOut = ApplicationWorkerOut
    BrokerOut = ApplicationBrokerOut
    AdminOut = ApplicationAdminOut

    AdminPaginatedOut = AdminPaginatedApplicationsOut
    WorkerPaginatedOut = WorkerPaginatedApplicationsOut
    BrokerPaginatedOut = BrokerPaginatedApplicationsOut
