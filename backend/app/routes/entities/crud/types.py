from typing import Protocol, runtime_checkable, TypeVar
from sqlalchemy.orm.session import Session
from uuid import UUID

from backend.app.schemas.entities import AdminSchema, BrokerSchema, WorkerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService

SchemaT = TypeVar(
    "SchemaT",
    AdminSchema.Create,
    AdminSchema.Update,
    AdminSchema.Out,
    AdminSchema.Base,
    WorkerSchema.Create,
    WorkerSchema.Update,
    WorkerSchema.Out,
    WorkerSchema.Base,
    BrokerSchema.Create,
    BrokerSchema.Update,
    BrokerSchema.Out,
    BrokerSchema.Base,
    ClientSchema.Create,
    ClientSchema.Update,
    ClientSchema.Out,
    ClientSchema.Base,
)

ServiceT = TypeVar(
    "ServiceT",
    AdminService,
    WorkerService,
    BrokerService,
    ClientService
)


@runtime_checkable
class BaseServiceProtocol(Protocol):
    def __init__(self, db: Session) -> None: ...

    def get_user_by_telegram_id(self, telegram_id: int) -> object: ...

    def create(self, data: SchemaT) -> SchemaT: ...

    def update(self, id: UUID, data: SchemaT) -> SchemaT: ...

    def delete(self, id: UUID) -> SchemaT: ...


__all__ = [
    "SchemaT",
    "ServiceT",
    "BaseServiceProtocol",
]
