from typing import Dict, Tuple, Optional, Type, TypeVar

from asyncpg.protocol.protocol import Protocol
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta

from app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from app.schemas.auth import LoginRequest
from app.schemas.sessions import TokenPair
from app.services.auth import PasswordService
from app.permissions import PermissionRole
from app.routes.auth.login.types import LoginTypes
from app.utils.protocols import BaseService, BaseSchemaNamespace
from app.models.entities import Admin, Worker, Broker, Client

class LoginTypesCls(BaseModel):
    web: Optional[Tuple[LoginTypes, Type[BaseModel], Type[BaseModel]]] = None
    bot: Optional[Tuple[LoginTypes, Type[BaseModel], Type[BaseModel]]] = None

class LoginWebResponse(BaseModel):
    status: int = 200

ModelT = Admin | Worker |Broker | Client

ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, BaseService, BaseSchemaNamespace, Type[ModelT], LoginTypesCls]] = {
    PermissionRole.ADMIN: (
        "/admin",
        PasswordService,
        AdminSchema,
        Admin,
        LoginTypesCls(
            web=(LoginTypes.WEB, LoginRequest, LoginWebResponse),
            bot=(LoginTypes.BOT, LoginRequest, TokenPair),
        )
    ),
    PermissionRole.WORKER: (
        "/worker",
        PasswordService,
        WorkerSchema,
        Worker,
        LoginTypesCls(
            web=(LoginTypes.WEB, LoginRequest, LoginWebResponse),
            bot=(LoginTypes.BOT, LoginRequest, TokenPair),
        )
    ),
    PermissionRole.BROKER: (
        "/broker",
        PasswordService,
        BrokerSchema,
        Broker,
        LoginTypesCls(
            web=(LoginTypes.WEB, LoginRequest, LoginWebResponse),
        )
    ),
    PermissionRole.CLIENT: (
        "/client",
        PasswordService,
        ClientSchema,
        Client,
        LoginTypesCls(
            bot=(LoginTypes.BOT, LoginRequest, TokenPair),
        )
    ),
}

__all__ = [
    "ROLE_REGISTRY",
]