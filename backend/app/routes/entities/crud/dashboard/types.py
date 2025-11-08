from dataclasses import Field
from uuid import UUID
from pydantic import BaseModel
from typing import List, Literal
from app.schemas.entities.client_schema import ClientOut, ClientWorkerOut, ClientBrokerOut, ClientAdminOut
from app.schemas.entities.broker_schema import BrokerOut, BrokerAdminOut
from app.schemas.entities.worker_schema import WorkerOut, WorkerAdminOut


class SimpleIntOut(BaseModel):
    value: int

class SimpleFloatOut(BaseModel):
    value: float

class StatusMessage(BaseModel):
    status: str

class WorkerClientListOut(BaseModel):
    clients: List[ClientWorkerOut]
    total: int

class BrokerClientListOut(BaseModel):
    clients: List[ClientBrokerOut]
    total: int

class ClientIdIn(BaseModel):
    client_id: UUID

class WorkerIdIn(BaseModel):
    worker_id: UUID

class BrokerIdIn(BaseModel):
    broker_id: UUID

class WorkerBucketClientsIn(BaseModel):
    worker_id: UUID
    skip: int = 0
    limit: int = 8

class BrokerBucketClientsIn(BaseModel):
    broker_id: UUID
    skip: int = 0
    limit: int = 8

class WorkerSignClientIn(BaseModel):
    client_id: UUID
    worker_id: UUID

class BrokerSignClientIn(BaseModel):
    client_id: UUID
    broker_id: UUID

class BrokerCreateCredit(BaseModel):
    client_id: UUID
    broker_id: UUID
    amount: float

class AdminIdIn(BaseModel):
    admin_id: UUID


class BucketIn(BaseModel):
    skip: int
    limit: int


# ─── PAGINATED OUTPUTS ──────────────────
class AdminPaginatedClientsOut(BaseModel):
    clients: List[ClientAdminOut]
    total: int


class AdminPaginatedWorkersOut(BaseModel):
    clients: List[WorkerAdminOut]
    total: int


class AdminPaginatedBrokersOut(BaseModel):
    clients: List[BrokerAdminOut]
    total: int


# ─── AGGREGATE SUMMARY ──────────────────
class AdminDashboardSummaryOut(BaseModel):
    clients: int
    brokers: int
    credits: int
    active_credits: int
    completed_credits: int
    issued_amount: int
    paid_amount: int

DeletedFilter = Literal["active", "only", "all"]
