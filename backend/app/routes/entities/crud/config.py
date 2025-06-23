# config.py
from typing import Tuple, List, Type, cast, Dict
from pydantic import BaseModel

from .types import BaseServiceProtocol, CRUDSchemas, TelegramId, CRUDOutputSchemas, CRUDInputSchemas, MatrixRow, \
    SuccessfulDeletedUser
from backend.app.permissions import PermissionRole
from backend.app.services.entities import (
    AdminService,
    BrokerService,
    WorkerService,
    ClientService,
)
from backend.app.schemas.entities import (
    AdminSchema,
    BrokerSchema,
    WorkerSchema,
    ClientSchema,
)

# ---------------------------------------------------------------------- #
# This dict contains base schema *namespaces* like `AdminSchema`
# ---------------------------------------------------------------------- #
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
                Read=TelegramId,
                Update=AdminSchema.Update,
                Delete=TelegramId,
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
                Read=TelegramId,
                Update=WorkerSchema.Update,
                Delete=TelegramId,
            ),
            output=CRUDOutputSchemas(
                Create=WorkerSchema.Out,
                Read=WorkerSchema.Out,
                Update=WorkerSchema.Out,
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
                Read=TelegramId,
                Update=BrokerSchema.Update,
                Delete=TelegramId,
            ),
            output=CRUDOutputSchemas(
                Create=BrokerSchema.Out,
                Read=BrokerSchema.Out,
                Update=BrokerSchema.Out,
                Delete=SuccessfulDeletedUser,
            ),
        ),
    ),
    PermissionRole.CLIENT: (
        "/client",
        cast(Type[BaseServiceProtocol], ClientService),
        CRUDSchemas(
            input=CRUDInputSchemas(
                Create=ClientSchema.Create,
                Read=TelegramId,
                Update=ClientSchema.Update,
                Delete=TelegramId,
            ),
            output=CRUDOutputSchemas(
                Create=ClientSchema.Out,
                Read=ClientSchema.Out,
                Update=ClientSchema.Out,
                Delete=SuccessfulDeletedUser,
            ),
        ),
    ),
}

# Map schema names to their respective CRUDSchemas attributes
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
    """
    Builds a CRUD matrix for a specific action (e.g. "Create", "Read", "Update", "Delete"),
    extracting corresponding input/output schemas from RoleSchemas.
    """
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


# Ready-to-use schema matrices
CREATE_MATRIX:     List[MatrixRow] = _build_matrix("Create")
READ_MATRIX:       List[MatrixRow] = _build_matrix("Read")
UPDATE_MATRIX:     List[MatrixRow] = _build_matrix("Update")
DELETE_MATRIX:     List[MatrixRow] = _build_matrix("Delete")

__all__ = [
    "CREATE_MATRIX",
    "READ_MATRIX",
    "UPDATE_MATRIX",
    "DELETE_MATRIX",
    "MatrixRow"
]
