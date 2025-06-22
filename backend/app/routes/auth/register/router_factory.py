from __future__ import annotations

from typing import Awaitable, Callable, List, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from uuid import UUID

from backend.app.routes.auth.register.types import RegisterTypes
from backend.app.routes.auth.register.config import ROLE_REGISTRY
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.utils.cookies import set_auth_cookies
from backend.app.utils.protocols import BaseService, BaseSchemaNamespace
from backend.db.session import get_async_db
from backend.app.routes.auth.register._base import generate_register_endpoints
from backend.app.permissions import PermissionRole
from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService

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


def make_register_handler(
        role: PermissionRole,
        register_type: RegisterTypes,
        service_class: Type[ServiceT],
        schema_class: Type[SchemaT],
        create_method_name: str,
) -> Callable[..., Awaitable]:
    """
    Generates a registration handler for a specific role and registration type (WEB or BOT).

    Args:
        role (PermissionRole): The role of the user (e.g., ADMIN, WORKER).
        register_type (RegisterTypes): The type of registration (WEB or BOT).
        service_class (Type[ServiceT]): The service class (e.g., AdminService).
        schema_class (Type[SchemaT]): The schema class for validation (e.g., AdminSchema).
        create_method_name (str): The method name for creating the user in the service class.

    Returns:
        Callable[..., Awaitable]: A callable that handles the registration request.
    """

    async def _handler(
            request_data: LoginRequest,
            request: Request,
            db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        svc = service_class(db)

        # Check if the required fields are provided
        email = request_data.email
        password = request_data.password

        if email is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Email address required")
        if password is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Password required")

        # Handle registration based on the register type
        if RegisterTypes.BOT == register_type:
            # Check if user already exists by Telegram ID (for BOT registration)
            if await svc.get_user_by_telegram_id(request_data.telegram_id):  # fixed typo
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
        elif RegisterTypes.WEB == register_type:
            # Check if user already exists by email (for WEB registration)
            if await svc.get_user_by_email(request_data.email):
                raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid register type provided")

        # Hash the password before saving to the database
        password_service = PasswordService(db)
        hashed_password = password_service.hash(password)

        # Dynamically call the create method based on the provided `create_method_name`
        create_method = getattr(svc, create_method_name)
        user = await create_method({"email": email, "password": hashed_password})  # Save user with hashed password

        # Generate access and refresh tokens
        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        # Prepare response based on the register type (WEB or BOT)
        if RegisterTypes.BOT == register_type:
            response = JSONResponse(content={"access_token": access, "refresh_token": refresh, "expires_in": ttl})
            set_auth_cookies(response, access, refresh, ttl)
        elif RegisterTypes.WEB == register_type:
            response = TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid register type provided")

        return response

    return _handler


def create_register_routers() -> List[APIRouter]:
    """
    This function generates the registration routes for each role,
    handling different registration types (WEB and BOT) dynamically.

    It iterates through the `ROLE_REGISTRY` dictionary, creates a route
    for each role and its corresponding registration types, and
    attaches the necessary handler to process requests.

    Returns:
        List[APIRouter]: A list of routers with all registration endpoints.
    """
    routers: List[APIRouter] = []

    # Iterate over all roles and their registration types
    for role, (path, register_addons) in ROLE_REGISTRY.items():
        router: APIRouter = APIRouter()  # Create a new router for the current role

        # Iterate through the list of registration types (e.g., WEB, BOT) for the current role
        for register_type, service, schema, create_method_name in register_addons:
            # Create a handler for the current register_type (WEB or BOT)
            handler = make_register_handler(
                role=role,
                register_type=register_type,  # Pass the current registration type (WEB or BOT)
                service_class=service,
                schema_class=schema,
                create_method_name=create_method_name,
            )

            # Generate a unique path for this registration type (e.g., /admin/register/web)
            register_path = f"{path}/register/{register_type.name.lower()}"
            tag_name = f"{role.value.lower()}-{register_type.name.lower()}"

            # Add the registration endpoint to the router
            generate_register_endpoints(
                router=router,
                path=register_path,
                handler=handler,
                tags=[tag_name],  # Clean tag for better readability in documentation
                rate_limit_rule="10/minute",  # Optional rate limit rule
                name=f"register_{role.value.lower()}_{register_type.name.lower()}",  # Meaningful handler names
            )

        routers.append(router)  # Add the router for this role to the list

    return routers  # Return the list of routers containing all registration endpoints

# TODO: Add one more LoginRequest for BOT and for WEB
