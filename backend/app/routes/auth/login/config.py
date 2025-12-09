from typing import Dict, Tuple, Optional, Type, TypeVar

from asyncpg.protocol.protocol import Protocol
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta

from app.schemas import AdminSchema, WorkerSchema, BrokerSchema
from app.schemas.auth import LoginRequest
from app.schemas.sessions import TokenPair
from app.services.auth import PasswordService
from app.permissions import PermissionRole
from app.routes.auth.login.types import LoginTypes
from app.utils.protocols import BaseService, BaseSchemaNamespace
from app.models.entities import Admin, Worker, Broker

class LoginTypesCls(BaseModel):
    web: Optional[Tuple[LoginTypes, Type[BaseModel], Type[BaseModel]]] = None
    bot: Optional[Tuple[LoginTypes, Type[BaseModel], Type[BaseModel]]] = None

class LoginWebResponse(BaseModel):
    status: int = 200

ModelT = Admin | Worker |Broker

ROLE_REGISTRY: Dict[PermissionRole, Tuple[str, BaseService, BaseSchemaNamespace, Type[ModelT], LoginTypesCls]] = {
    PermissionRole.ADMIN: (
        "/admin",
        PasswordService,
        AdminSchema,
        Admin,
        LoginTypesCls(
            web=(LoginTypes.WEB, LoginRequest, LoginWebResponse),
        )
    ),
    PermissionRole.WORKER: (
        "/worker",
        PasswordService,
        WorkerSchema,
        Worker,
        LoginTypesCls(
            web=(LoginTypes.WEB, LoginRequest, LoginWebResponse),
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
}

__all__ = [
    "ROLE_REGISTRY",
]