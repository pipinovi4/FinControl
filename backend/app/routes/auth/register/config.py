from typing import Dict, Tuple, Optional, Type
from pydantic import BaseModel

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema, UserSchema
from backend.app.schemas.sessions import TokenPair
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService
from backend.app.permissions import PermissionRole
from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.utils.protocols import BaseSchemaNamespace, BaseService

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
            bot=(RegisterTypes.BOT, AdminSchema.Create, TokenPair)
        ),
    ),
    PermissionRole.WORKER: (
        "/worker",
        WorkerService,
        WorkerSchema,
        RegisterTypesCls(
            web=(RegisterTypes.WEB, WorkerSchema.Create, WorkerSchema.WebRegisterResponse),
            bot=(RegisterTypes.BOT, WorkerSchema.Create, TokenPair)
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
    PermissionRole.CLIENT: (
        "/client",
        ClientService,
        ClientSchema,
        RegisterTypesCls(
            bot=(RegisterTypes.BOT, ClientSchema.WebRegisterRequest, TokenPair)
        ),
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]
