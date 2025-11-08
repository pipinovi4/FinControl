from typing import Protocol, runtime_checkable, TypeVar, Union, Type, Tuple, NamedTuple, TypedDict
from sqlalchemy.orm.session import Session
from pydantic import BaseModel
from uuid import UUID

from app.permissions import PermissionRole
from app.schemas.entities import AdminSchema, BrokerSchema, WorkerSchema, ClientSchema
from app.services.entities import AdminService, WorkerService, BrokerService, ClientService

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

    def create(self, data: SchemaT) -> SchemaT: ...

    def update(self, id: UUID, data: SchemaT) -> SchemaT: ...

    def delete(self, id: UUID) -> SchemaT: ...

class EntityID(BaseModel):
    id: UUID

class SuccessfulDeletedUser(BaseModel):
    message: str

class CRUDInputSchemas(NamedTuple):
    Create: Type[Union[BrokerSchema.Create, WorkerSchema.Create, BrokerSchema.Update, ClientSchema.Create]]
    Read: Type[EntityID]
    Update: Type[Union[AdminSchema.Update, WorkerSchema.Update, BrokerSchema.Update, ClientSchema.Update]]
    Delete: Type[EntityID]

class CRUDOutputSchemas(NamedTuple):
    Create: Type[Union[BrokerSchema.Out, WorkerSchema.Out, BrokerSchema.Out, ClientSchema.Out]]
    Read: Type[Union[BrokerSchema.Out, WorkerSchema.Out, BrokerSchema.Out, ClientSchema.Out]]
    Update: Type[Union[BrokerSchema.Out, WorkerSchema.Out, BrokerSchema.Out, ClientSchema.Out]]
    Delete: Type[SuccessfulDeletedUser]

class CRUDSchemas(NamedTuple):
    input: CRUDInputSchemas
    output: CRUDOutputSchemas

MatrixRow = Tuple[
    PermissionRole,
    str,
    Type[BaseServiceProtocol],
    Type[BaseModel],  # input schema
    Type[BaseModel],  # output schema
]
__all__ = [
    "SchemaT",
    "ServiceT",
    "BaseServiceProtocol",
    "EntityID",
    "CRUDSchemas",
    "CRUDInputSchemas",
    "CRUDOutputSchemas",
    "MatrixRow",
    "SuccessfulDeletedUser"
]
