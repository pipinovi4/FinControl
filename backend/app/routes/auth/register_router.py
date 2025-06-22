from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Type, TypeVar

from backend.app.utils.cookies import set_auth_cookies
from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema, UserSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService
from backend.app.utils.middlewares import rate_limit
from backend.db.session import get_async_db
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import generate_token_pair
from backend.app.utils.decorators import handle_route_exceptions

register_router = APIRouter(tags=["Register"])

SchemaT = TypeVar(
    "SchemaT",
    AdminSchema.Create,
    WorkerSchema.Create,
    BrokerSchema.Create,
    ClientSchema.Create
)

ServiceT = TypeVar(
    "ServiceT",
    AdminService,
    WorkerService,
    BrokerService,
    ClientService
)

def generate_register_handler(
    path: str,
    service_class: Type[ServiceT],
    schema_class: Type[SchemaT],
    create_method_name: str,
):
    @handle_route_exceptions
    @rate_limit("3/minute")
    @register_router.post(
        path,
        response_model=TokenPair,
        summary=f"Register a new {path.strip('/').capitalize()} and get tokens",
        status_code=status.HTTP_201_CREATED,
    )
    async def register(
        payload: schema_class, # type: ignore
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> JSONResponse:
        svc = service_class(db)

        if await svc.get_user_by_telegram_id(payload.telegram_id): # type: ignore
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"{path.strip('/').capitalize()} already exists")

        create_method = getattr(svc, create_method_name)
        user = await create_method(payload)

        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        response = JSONResponse(content={"access_token": access, "refresh_token": refresh, "expires_in": ttl})

        set_auth_cookies(response, access, refresh, ttl)

        return response
