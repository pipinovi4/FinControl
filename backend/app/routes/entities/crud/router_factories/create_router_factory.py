from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.db.session import get_db
from backend.app.permissions import PermissionRole
from backend.app.routes.entities.crud.config import CREATE_MATRIX
from backend.app.routes.entities.crud._base import generate_crud_endpoints
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.routes.entities.crud.types import ServiceT


def make_create_handler(
    service_cls: Type[ServiceT],
    schema_cls: Type[BaseModel],
    role: PermissionRole,
) -> Callable:
    @handle_route_exceptions()
    async def handler(
        payload: schema_cls,               # type: ignore
        request: Request,
        db: Session = Depends(get_db),
    ) -> schema_cls:                       # type: ignore
        svc = service_cls(db)

        if svc.get_user_by_telegram_id(payload.telegram_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"{role.value.title()} with this telegram_id already exists",
            )

        return svc.create(payload)         # або .create_user(...)
    return handler

def create_router_factory() -> APIRouter:
    router = APIRouter(prefix="/create", tags=["Create Entities"])

    for role, path, service_cls, schema_ns in CREATE_MATRIX:
        handler = make_create_handler(cast(Type[ServiceT], service_cls), schema_ns, role)

        generate_crud_endpoints(
            router=router,
            verb="post",
            path=path,
            handler=handler,
            input_schema=schema_ns,
            tags=[role.value],
        )

    return router
