from typing import Dict, Tuple, List

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService
from backend.app.permissions import PermissionRole
from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.utils.protocols import BaseSchemaNamespace, BaseService

ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, Tuple[List[RegisterTypes], BaseService, BaseSchemaNamespace, str]]] = {
    PermissionRole.ADMIN: (
        "/admin",  # Path for admin register
        (
            [RegisterTypes.WEB, RegisterTypes.BOT],  # Register types for Admin
            AdminService,  # Service for Admin
            AdminSchema,  # Schema for Admin
            "admin_registration_handler",  # Handler name for Admin
        )
    ),
    PermissionRole.WORKER: (
        "/worker",  # Path for worker register
        (
            [RegisterTypes.WEB, RegisterTypes.BOT],  # Register types for Worker
            WorkerService,  # Service for Worker
            WorkerSchema,  # Schema for Worker
            "worker_registration_handler",  # Handler name for Worker
        )
    ),
    PermissionRole.CLIENT: (
        "/client",  # Path for client register
        (
            [RegisterTypes.BOT],  # Register type for Client
            ClientService,  # Service for Client
            ClientSchema,  # Schema for Client
            "client_registration_handler",  # Handler name for Client
        )
    ),
    PermissionRole.BROKER: (
        "/broker",  # Path for broker register
        (
            [RegisterTypes.WEB],  # Register type for Broker
            BrokerService,  # Service for Broker
            BrokerSchema,  # Schema for Broker
            "broker_registration_handler",  # Handler name for Broker
        )
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]
