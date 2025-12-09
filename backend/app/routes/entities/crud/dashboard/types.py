# backend/app/routes/entities/crud/dashboard/types.py

from uuid import UUID
from typing import List, Literal
from pydantic import BaseModel

from app.schemas.entities.application_schema import (
    ApplicationWorkerOut,
    ApplicationBrokerOut,
    ApplicationAdminOut,
)
from app.schemas.entities.worker_schema import WorkerAdminOut
from app.schemas.entities.broker_schema import BrokerAdminOut


# ─────────────────────────────────────────
# SIMPLE OUTPUT TYPES
# ─────────────────────────────────────────

class SimpleIntOut(BaseModel):
    value: int


class SimpleFloatOut(BaseModel):
    value: float


class StatusMessage(BaseModel):
    status: str


# ─────────────────────────────────────────
# PAGINATED LISTS (WORKER / BROKER)
# ─────────────────────────────────────────

class WorkerApplicationListOut(BaseModel):
    applications: List[ApplicationWorkerOut]
    total: int


class BrokerApplicationListOut(BaseModel):
    applications: List[ApplicationBrokerOut]
    total: int


# ─────────────────────────────────────────
# INPUT MODELS (IDS, BUCKETS)
# ─────────────────────────────────────────

class ApplicationIdIn(BaseModel):
    application_id: UUID


class WorkerIdIn(BaseModel):
    worker_id: UUID


class BrokerIdIn(BaseModel):
    broker_id: UUID


class WorkerBucketApplicationsIn(BaseModel):
    worker_id: UUID
    skip: int = 0
    limit: int = 8


class BrokerBucketApplicationsIn(BaseModel):
    broker_id: UUID
    skip: int = 0
    limit: int = 8


class WorkerAssignApplicationIn(BaseModel):
    application_id: UUID
    worker_id: UUID


class BrokerAssignApplicationIn(BaseModel):
    application_id: UUID
    broker_id: UUID


class BrokerCreateCredit(BaseModel):
    application_id: UUID
    broker_id: UUID
    amount: float


class AdminIdIn(BaseModel):
    admin_id: UUID


class BucketIn(BaseModel):
    skip: int
    limit: int


# ─────────────────────────────────────────
# ADMIN PAGINATED OUTPUTS
# ─────────────────────────────────────────

class AdminPaginatedApplicationsOut(BaseModel):
    applications: List[ApplicationAdminOut]
    total: int


class AdminPaginatedWorkersOut(BaseModel):
    workers: List[WorkerAdminOut]
    total: int


class AdminPaginatedBrokersOut(BaseModel):
    brokers: List[BrokerAdminOut]
    total: int


# ─────────────────────────────────────────
# ADMIN SUMMARY
# ─────────────────────────────────────────

class AdminDashboardSummaryOut(BaseModel):
    applications: int
    brokers: int
    credits: int
    active_credits: int
    completed_credits: int
    issued_amount: int
    paid_amount: int


DeletedFilter = Literal["active", "only", "all"]
