# config.py
from typing import Tuple, List, Type, cast, Dict
from pydantic import BaseModel

from .types import (
    BaseServiceProtocol,
    CRUDSchemas,
    CRUDOutputSchemas,
    CRUDInputSchemas,
    MatrixRow,
    SuccessfulDeletedUser,
    EntityID
)
from app.permissions import PermissionRole
from app.services.entities import (
    AdminService,
    BrokerService,
    WorkerService,
)
from app.schemas.entities import (
    AdminSchema,
    BrokerSchema,
    WorkerSchema,
)

ROLE_REGISTRY: Dict[
    PermissionRole,
    Tuple[str, Type[BaseServiceProtocol], CRUDSchemas]
] = {
    PermissionRole.ADMIN: (
        "/admin",
        cast(Type[BaseServiceProtocol], AdminService),
        CRUDSchemas(
            input=CRUDInputSchemas(
                Create=AdminSchema.Create,
                Read=EntityID,
                Update=AdminSchema.Update,
                Delete=EntityID,
            ),
            output=CRUDOutputSchemas(
                Create=AdminSchema.Out,
                Read=AdminSchema.Out,
                Update=AdminSchema.Out,
                Delete=SuccessfulDeletedUser,
            ),
        ),
    ),

    PermissionRole.WORKER: (
        "/worker",
        cast(Type[BaseServiceProtocol], WorkerService),
        CRUDSchemas(
            input=CRUDInputSchemas(
                Create=WorkerSchema.Create,
                Read=EntityID,
                Update=WorkerSchema.Update,
                Delete=EntityID,
            ),
            output=CRUDOutputSchemas(
                Create=WorkerSchema.Short,
                Read=WorkerSchema.Short,
                Update=WorkerSchema.Short,
                Delete=SuccessfulDeletedUser,
            ),
        ),
    ),

    PermissionRole.BROKER: (
        "/broker",
        cast(Type[BaseServiceProtocol], BrokerService),
        CRUDSchemas(
            input=CRUDInputSchemas(
                Create=BrokerSchema.Create,
                Read=EntityID,
                Update=BrokerSchema.Update,
                Delete=EntityID,
            ),
            output=CRUDOutputSchemas(
                Create=BrokerSchema.Short,
                Read=BrokerSchema.Short,
                Update=BrokerSchema.Short,
                Delete=SuccessfulDeletedUser,
            ),
        ),
    ),
}

# ──────────────────────────────────────────────────────────────
# MATRIX BUILDERS
# ──────────────────────────────────────────────────────────────

SCHEMA_SELECTOR = {
    "Create": lambda schemas: schemas.input.Create,
    "Read":   lambda schemas: schemas.input.Read,
    "Update": lambda schemas: schemas.input.Update,
    "Delete": lambda schemas: schemas.input.Delete,
    "CreateOut": lambda schemas: schemas.output.Create,
    "ReadOut":   lambda schemas: schemas.output.Read,
    "UpdateOut": lambda schemas: schemas.output.Update,
    "DeleteOut": lambda schemas: schemas.output.Delete,
}

def _build_matrix(schema_action: str) -> List[MatrixRow]:
    return [
        (
            role,
            path,
            service,
            getattr(schemas.input, schema_action),
            getattr(schemas.output, schema_action),
        )
        for role, (path, service, schemas) in ROLE_REGISTRY.items()
    ]

CREATE_MATRIX  = _build_matrix("Create")
READ_MATRIX    = _build_matrix("Read")
UPDATE_MATRIX  = _build_matrix("Update")
DELETE_MATRIX  = _build_matrix("Delete")

__all__ = [
    "CREATE_MATRIX",
    "READ_MATRIX",
    "UPDATE_MATRIX",
    "DELETE_MATRIX",
    "MatrixRow"
]
