from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic.main import BaseModel

from backend.db.session import get_db
from backend.app.permissions import PermissionRole
from backend.app.routes.entities.crud.config import UPDATE_MATRIX
from backend.app.routes.entities.crud._base import generate_crud_endpoints
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.routes.entities.crud.types import ServiceT


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
        db: Session = Depends(get_db),
    ) -> schema_cls:  # type: ignore
        svc = service_cls(db)
        entity = svc.update(id, payload)
        if not entity:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{role.value.title()} with id '{id}' not found",
            )
        return entity
    return handler


def update_router_factory() -> APIRouter:
    router = APIRouter(prefix="/update", tags=["Update Entities"])

    for role, path, service_cls, schema_cls in UPDATE_MATRIX:
        handler = make_update_handler(cast(Type[ServiceT], service_cls), schema_cls, role)

        generate_crud_endpoints(
            router=router,
            verb="put",
            path=path + "/{id}",
            handler=handler,
            input_schema=schema_cls,
            tags=[role.value],
        )

    return router
