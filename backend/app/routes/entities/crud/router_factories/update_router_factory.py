from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from backend.db.session import get_async_db
from app.permissions import PermissionRole
from app.routes.entities.crud.config import UPDATE_MATRIX
from app.routes.entities.crud._base import generate_crud_endpoints
from app.utils.decorators import handle_route_exceptions
from app.routes.entities.crud.types import ServiceT


def make_update_handler(
    service_cls: Type[ServiceT],
    schema_cls: Type[BaseModel],
    role: PermissionRole,
) -> Callable:
    @handle_route_exceptions()
    async def handler(
        id: str,
        payload: schema_cls,  # type: ignore
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> schema_cls:  # type: ignore
        svc = service_cls(db)
        entity = await svc.update(id, payload)
        if not entity:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{role.value.title()} with id '{id}' not found",
            )
        return entity

    return handler


def update_router_factory() -> APIRouter:
    router = APIRouter(prefix="/update", tags=["Update Entities"])

    for role, path, service_cls, input_schema, output_schema in UPDATE_MATRIX:
        handler = make_update_handler(cast(Type[ServiceT], service_cls), input_schema, role)

        generate_crud_endpoints(
            router=router,
            verb="put",
            path=path + "/{id}",
            handler=handler,
            schema_request=input_schema,
            schema_response=output_schema,
            tags=[role.value],
            rate_limit_rule="20/minute",
            name=f"update_{role.value.lower()}",
        )

    return router
