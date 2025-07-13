from typing import Awaitable, Callable, List, Type, TypeVar, cast, Any
from fastapi import APIRouter, HTTPException, Request, Depends, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import UUID

from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.routes.auth.register.config import ROLE_REGISTRY
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import generate_token_pair
from backend.app.utils.cookies import set_auth_cookies
from backend.db.session import get_async_db
from backend.app.routes.auth.register._base import generate_register_endpoints
from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService

# Type variables for generic schemas and services
SchemaT = TypeVar("SchemaT", AdminSchema, WorkerSchema, BrokerSchema, ClientSchema)
ServiceT = TypeVar("ServiceT", AdminService, WorkerService, BrokerService, ClientService)


def make_register_handler(
    register_type: RegisterTypes,
    service_cls: Type[ServiceT],
    schema_cls: Type[SchemaT],
    input_schema: Type[BaseModel],
) -> Callable[..., Awaitable[Any]]:
    """
    Factory for creating a FastAPI handler for registration.

    Args:
        register_type (RegisterTypes): The type of registration (BOT or WEB).
        service_cls (Type[ServiceT]): The service class to handle user creation.
        schema_cls (Type[SchemaT]): The schema class containing Create submodel.
        input_schema (Type[BaseModel]): The request model to parse input.

    Returns:
        FastAPI route handler function.
    """
    async def handler(
        request: Request,
        data: input_schema = Body(...),
        db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        payload = schema_cls.Create(**data.model_dump())
        service = service_cls(db)

        if not payload.email or not payload.password:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Missing email or password")

        # Check if a user already exists
        if register_type == RegisterTypes.BOT:
            if await service.get_by_telegram_id(payload.telegram_id):
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
        elif register_type == RegisterTypes.WEB:
            if await service.get_by_email(payload.email):
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")

        # Hash password and create a user
        user = await service.create(schema_cls.Create(**payload.model_dump()))

        user = await service.get_by_id(user.id)

        # Token generation
        access, refresh, expires_in = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        if register_type == RegisterTypes.WEB:
            response = JSONResponse(content=
                jsonable_encoder(schema_cls.WebRegisterResponse.model_validate(user))
            )
            set_auth_cookies(response, access, refresh, expires_in)
            return response

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=expires_in)

    return handler


def create_register_routers() -> List[APIRouter]:
    """
    Creates FastAPI routers for registration endpoints for each role and register type.
    Uses ROLE_REGISTRY config.

    Returns:
        List[APIRouter]: A list of configured routers.
    """
    routers: List[APIRouter] = []

    for role, (base_path, service_cls, schema_cls, register_types) in ROLE_REGISTRY.items():
        router = APIRouter()

        for method in ("web", "bot"):
            register_info = getattr(register_types, method)
            if not register_info:
                continue

            reg_type, input_schema, output_schema = register_info

            route_handler = make_register_handler(
                register_type=reg_type,
                service_cls=cast(Type[ServiceT], service_cls),
                schema_cls=cast(Type[SchemaT], schema_cls),
                input_schema=input_schema,
            )

            full_path = f"{base_path}/{reg_type.name.lower()}"
            tag = f"{role.value.lower()}-{reg_type.name.lower()}"

            generate_register_endpoints(
                router=router,
                path=full_path,
                handler=route_handler,
                tags=["Auth", tag],
                rate_limit_rule="10/minute",
                name=f"register_{role.value.lower()}_{reg_type.name.lower()}",
                input_model=input_schema,
                response_model=output_schema,
                schema_cls=schema_cls
            )

        routers.append(router)

    return routers
