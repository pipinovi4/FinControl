from typing import Type, Callable, cast
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_async_db
from backend.app.permissions import PermissionRole
from backend.app.routes.entities.crud.config import DELETE_MATRIX
from backend.app.routes.entities.crud._base import generate_crud_endpoints
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.routes.entities.crud.types import ServiceT


def make_delete_handler(
    service_cls: Type[ServiceT],
    role: PermissionRole,
) -> Callable:
    @handle_route_exceptions()
    async def handler(
        id: str,
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> dict:
        svc = service_cls(db)
        success = await svc.delete(id)
        if not success:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{role.value.title()} with id '{id}' not found",
            )
        return {"detail": f"{role.value.title()} deleted"}

    return handler


def delete_router_factory() -> APIRouter:
    router = APIRouter(prefix="/delete", tags=["Delete Entities"])

    for role, path, service_cls, _ in DELETE_MATRIX:
        handler = make_delete_handler(cast(Type[ServiceT], service_cls), role)

        generate_crud_endpoints(
            router=router,
            verb="delete",
            path=path + "/{id}",
            handler=handler,
            rate_limit_rule="20/minute",
            tags=[role.value],
            name=f"create_{role.value.lower()}",
        )

    return router
