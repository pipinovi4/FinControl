from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from backend.db.session import get_async_db
from backend.app.permissions import PermissionRole
from backend.app.routes.entities.crud.config import READ_MATRIX
from backend.app.routes.entities.crud._base import generate_crud_endpoints
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.routes.entities.crud.types import ServiceT


def make_read_handler(
    service_cls: Type[ServiceT],
    schema_cls: Type[BaseModel],
    role: PermissionRole,
) -> Callable:
    @handle_route_exceptions()
    async def handler(
        id: str,
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> schema_cls:  # type: ignore
        svc = service_cls(db)
        entity = await svc.get_by_id(id)
        if not entity:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{role.value.title()} with id '{id}' not found",
            )
        return entity

    return handler


def read_router_factory() -> APIRouter:
    router = APIRouter(prefix="/read", tags=["Read Entities"])

    for role, path, service_cls, schema_cls in READ_MATRIX:
        handler = make_read_handler(cast(Type[ServiceT], service_cls), schema_cls, role)

        generate_crud_endpoints(
            router=router,
            verb="get",
            path=path + "/{id}",
            handler=handler,
            tags=[role.value],
            rate_limit_rule="20/minute",
            name=f"create_{role.value.lower()}",
        )

    return router
