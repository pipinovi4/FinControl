# types.py
from typing import Protocol, runtime_checkable, TypeVar, Union, Type, Tuple, NamedTuple
from sqlalchemy.orm.session import Session
from pydantic import BaseModel
from uuid import UUID

from app.permissions import PermissionRole
from app.schemas.entities import (
    AdminSchema,
    BrokerSchema,
    WorkerSchema,
)
from app.services.entities import (
    AdminService,
    WorkerService,
    BrokerService,
)

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
)

ServiceT = TypeVar(
    "ServiceT",
    AdminService,
    WorkerService,
    BrokerService,
)

@runtime_checkable
class BaseServiceProtocol(Protocol):
    def __init__(self, db: Session) -> None: ...

    async def create(self, data: SchemaT) -> SchemaT: ...
    async def update(self, id: UUID, data: SchemaT) -> SchemaT: ...
    async def delete(self, id: UUID) -> SchemaT: ...

class EntityID(BaseModel):
    id: UUID

class SuccessfulDeletedUser(BaseModel):
    message: str

class CRUDInputSchemas(NamedTuple):
    Create: Type[
        Union[
            AdminSchema.Create,
            WorkerSchema.Create,
            BrokerSchema.Create,
        ]
    ]
    Read: Type[EntityID]
    Update: Type[
        Union[
            AdminSchema.Update,
            WorkerSchema.Update,
            BrokerSchema.Update,
        ]
    ]
    Delete: Type[EntityID]

class CRUDOutputSchemas(NamedTuple):
    Create: Type[
        Union[
            AdminSchema.Out,
            WorkerSchema.Out,
            BrokerSchema.Out,
        ]
    ]
    Read: Type[
        Union[
            AdminSchema.Out,
            WorkerSchema.Out,
            BrokerSchema.Out,
        ]
    ]
    Update: Type[
        Union[
            AdminSchema.Out,
            WorkerSchema.Out,
            BrokerSchema.Out,
        ]
    ]
    Delete: Type[SuccessfulDeletedUser]

class CRUDSchemas(NamedTuple):
    input: CRUDInputSchemas
    output: CRUDOutputSchemas

MatrixRow = Tuple[
    PermissionRole,
    str,
    Type[BaseServiceProtocol],
    Type[BaseModel],
    Type[BaseModel],
]
