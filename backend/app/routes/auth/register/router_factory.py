from __future__ import annotations

from typing import Awaitable, Callable, List, Type, TypeVar, cast, Annotated
from fastapi import APIRouter, HTTPException, Request, Depends, status, Body
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.routes.auth.register.config import ROLE_REGISTRY
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.utils.cookies import set_auth_cookies
from backend.db.session import get_async_db
from backend.app.routes.auth.register._base import generate_register_endpoints
from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService

# Type definitions for generic schema and service
SchemaT = TypeVar("SchemaT", AdminSchema, WorkerSchema, BrokerSchema, ClientSchema)
ServiceT = TypeVar("ServiceT", AdminService, WorkerService, BrokerService, ClientService)

def make_register_handler(
    register_type: RegisterTypes,
    service_class: Type[ServiceT],
    schema_class: SchemaT,
    create_method_name: str,
) -> Callable[..., Awaitable[JSONResponse | TokenPair]]:
    """
    Creates an async handler for user registration per role and register type (BOT/WEB).
    Handles:
    - Validation
    - Password hashing
    - User creation
    - Token generation
    - Cookie setting (for bots)
    """

    async def _handler(
        request: Request,
        request_data: schema_class.Create = Body(...),
        db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        svc = service_class(db)
        email = request_data.email
        password = request_data.password

        if not email or not password:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Missing email or password")

        # Validate existing user by register type
        if register_type == RegisterTypes.BOT:
            if await svc.get_user_by_telegram_id(request_data.telegram_id):
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
        elif register_type == RegisterTypes.WEB:
            if await svc.get_user_by_email(email):
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid register type")

        # Hash the password
        password_service = PasswordService(db)
        hashed_password = password_service.hash(password)

        # Create user dynamically
        create_method = getattr(svc, create_method_name)
        user = await create_method({"email": email, "password": hashed_password})

        # Generate access/refresh tokens
        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        # Response logic per register type
        if register_type == RegisterTypes.BOT:
            response = JSONResponse(content={
                "access_token": access,
                "refresh_token": refresh,
                "expires_in": ttl
            })
            set_auth_cookies(response, access, refresh, ttl)
            return response

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)

    return _handler

def create_register_routers() -> List[APIRouter]:
    """
    Creates register routers for each defined role and register type
    using config from ROLE_REGISTRY. Registers route with:
    - Typed input schema
    - Output token schema
    - Dynamic tags
    - Rate limit
    """
    routers: List[APIRouter] = []

    for role, (path, service, schema, create_method_name, register_types) in ROLE_REGISTRY.items():
        router = APIRouter()

        for register_type in register_types:
            handler = make_register_handler(
                register_type=register_type,
                service_class=cast(Type[ServiceT], service),
                schema_class=cast(Type[SchemaT], schema),
                create_method_name=create_method_name,
            )

            register_path = f"{path}/{register_type.name.lower()}"
            tag_name = f"{role.value.lower()}-{register_type.name.lower()}"

            generate_register_endpoints(
                router=router,
                path=register_path,
                handler=handler,
                tags=["Auth", tag_name],
                rate_limit_rule="10/minute",
                name=f"register_{role.value.lower()}_{register_type.name.lower()}",
                schema=cast(SchemaT, schema),
            )

        routers.append(router)

    return routers
