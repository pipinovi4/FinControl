# config.py
from typing import Tuple, List, Type, cast
from pydantic import BaseModel

from .types import BaseServiceProtocol, BaseSchemaNamespace
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
# MatrixRow = (role, path, service class, concrete schema class)
# ---------------------------------------------------------------------- #
MatrixRow = Tuple[PermissionRole, str, Type[BaseServiceProtocol], Type[BaseModel]]

# ---------------------------------------------------------------------- #
# This dict contains base schema *namespaces* like `AdminSchema`
# ---------------------------------------------------------------------- #
ROLE_REGISTRY: dict[PermissionRole, tuple[str, Type[BaseServiceProtocol], Type[BaseSchemaNamespace]]] = {
    PermissionRole.ADMIN:  ("/admin",  cast(Type[BaseServiceProtocol], AdminService),  AdminSchema),
    PermissionRole.WORKER: ("/worker", cast(Type[BaseServiceProtocol], WorkerService), WorkerSchema),
    PermissionRole.BROKER: ("/broker", cast(Type[BaseServiceProtocol], BrokerService), BrokerSchema),
    PermissionRole.CLIENT: ("/client", cast(Type[BaseServiceProtocol], ClientService), ClientSchema),
}

# Utility to build any CRUD matrix from ROLE_REGISTRY
# schema_attr must match class attribute names in the schema namespace
def _build_matrix(schema_attr: str) -> List[MatrixRow]:
    """
    Generate a CRUD matrix.

    Args:
        schema_attr: Name of the schema class inside each namespace
                     ('Create', 'Out', 'Update', 'Base', etc.).

    Returns:
        List of tuples: (role, URL prefix, service class, concrete schema class)
    """
    return [
        (role, path, svc, getattr(schema_ns, schema_attr))
        for role, (path, svc, schema_ns) in ROLE_REGISTRY.items()
    ]

# Ready-to-use matrices for router factories
CREATE_MATRIX:  List[MatrixRow] = _build_matrix("Create")
READ_MATRIX:    List[MatrixRow] = _build_matrix("Base")
UPDATE_MATRIX:  List[MatrixRow] = _build_matrix("Update")
DELETE_MATRIX:  List[MatrixRow] = _build_matrix("Base")  # or "Out", depending on your design

__all__ = [
    "CREATE_MATRIX",
    "READ_MATRIX",
    "UPDATE_MATRIX",
    "DELETE_MATRIX",
    "ROLE_REGISTRY",
    "MatrixRow"
]
