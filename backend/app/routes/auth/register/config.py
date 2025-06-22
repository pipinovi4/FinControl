from typing import Dict, Tuple, List

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService
from backend.app.permissions import PermissionRole
from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.utils.protocols import BaseSchemaNamespace, BaseService


ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, BaseService, BaseSchemaNamespace, str, List[RegisterTypes]]] = {
    PermissionRole.ADMIN: (
        "/admin",  # Path for admin register
        AdminService,  # Service for Admin
        AdminSchema,  # Schema for Admin
        "create_admin",  # Method name for Admin
        [RegisterTypes.WEB, RegisterTypes.BOT],  # Register types for Admin
    ),
    PermissionRole.WORKER: (
        "/worker",  # Path for worker register
        WorkerService,  # Service for Worker
        WorkerSchema,  # Schema for Worker
        "create_worker",  # Method name for Worker
        [RegisterTypes.WEB, RegisterTypes.BOT],  # Register types for Worker
    ),
    PermissionRole.CLIENT: (
        "/client",  # Path for client register
        ClientService,  # Service for Client
        ClientSchema,  # Schema for Client
        "create_client",  # Method name for Client
        [RegisterTypes.BOT],  # Register type for Client
    ),
    PermissionRole.BROKER: (
        "/broker",  # Path for broker register
        BrokerService,  # Service for Broker
        BrokerSchema,  # Schema for Broker
        "create_broker",  # Method name for Broker
        [RegisterTypes.WEB],  # Register type for Broker
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]
