from typing import Dict, Tuple, Optional, Type
from pydantic import BaseModel

from app.schemas import AdminSchema, WorkerSchema, BrokerSchema
from app.services.entities import AdminService, WorkerService, BrokerService
from app.permissions import PermissionRole
from app.routes.auth.register.types import RegisterTypes
from app.utils.protocols import BaseSchemaNamespace, BaseService

class RegisterTypesCls(BaseModel):
    web: Optional[Tuple[RegisterTypes, Type[BaseModel], Type[BaseModel]]] = None
    bot: Optional[Tuple[RegisterTypes, Type[BaseModel], Type[BaseModel]]] = None

class RegisterWebResponse(BaseModel):
    status: int = 200

ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, BaseService, BaseSchemaNamespace, RegisterTypesCls]] = {
    PermissionRole.ADMIN: (
        "/admin",
        AdminService,
        AdminSchema,
        RegisterTypesCls(
            web=(RegisterTypes.WEB, AdminSchema.Create, AdminSchema.WebRegisterResponse),
        ),
    ),
    PermissionRole.WORKER: (
        "/worker",
        WorkerService,
        WorkerSchema,
        RegisterTypesCls(
            web=(RegisterTypes.WEB, WorkerSchema.Create, WorkerSchema.WebRegisterResponse),
        ),
    ),
    PermissionRole.BROKER: (
        "/broker",
        BrokerService,
        BrokerSchema,
        RegisterTypesCls(
            web=(RegisterTypes.WEB, BrokerSchema.Create, BrokerSchema.WebRegisterResponse),
        ),
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]
