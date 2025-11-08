from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from backend.db.session import get_async_db
from app.permissions import PermissionRole
from app.routes.entities.crud.config import CREATE_MATRIX
from app.routes.entities.crud._base import generate_crud_endpoints
from app.utils.decorators import handle_route_exceptions
from app.routes.entities.crud.types import ServiceT


def make_create_handler(
    service_cls: Type[ServiceT],
    schema_cls: Type[BaseModel],
    role: PermissionRole,
) -> Callable:
    @handle_route_exceptions()
    async def handler(
        payload: schema_cls,  # type: ignore
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> schema_cls:  # type: ignore
        svc = service_cls(db)

        if await svc.get_by_email(payload.email):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"{role.value.title()} with this email already exists",
            )

        return await svc.create(payload)

    return handler


def create_router_factory() -> APIRouter:
    router = APIRouter(prefix="/create", tags=["Create Entities"])

    for role, path, service_cls, input_schema, output_schema in CREATE_MATRIX:
        handler = make_create_handler(cast(Type[ServiceT], service_cls), input_schema, role)

        generate_crud_endpoints(
            router=router,
            verb="post",
            path=path,
            handler=handler,
            schema_request=input_schema,
            schema_response=output_schema,
            tags=[role.value],
            rate_limit_rule="20/minute",
            name=f"create_{role.value.lower()}",
        )

    return router
