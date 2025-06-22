from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Type, TypeVar

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema, UserSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientService
from backend.app.utils.middlewares import rate_limit
from backend.db.session import get_async_db
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import generate_token_pair, PasswordService
from backend.app.utils.decorators import handle_route_exceptions

register_router = APIRouter(tags=["Register"])

# Define TypeVars for schemas and service classes to make the registration handler flexible
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
    # This decorator handles route-specific exceptions and ensures rate limiting.
    @handle_route_exceptions
    @rate_limit("3/minute")  # Limit the number of requests to prevent abuse
    @register_router.post(
        path,
        response_model=TokenPair,
        summary=f"Register a new {path.strip('/').capitalize()} and get tokens",
        status_code=status.HTTP_201_CREATED,
    )
    async def register(
        register_data: Type[schema_class],
        request: Request,  # We will receive the registration data from the request body
        db: AsyncSession = Depends(get_async_db),
    ) -> TokenPair:
        svc = service_class(db)

        # Check if the required fields are provided
        email = register_data.email
        password = register_data.password

        # Check if the email is already registered
        if await svc.get_user_by_email(email):  # type: ignore
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"{path.strip('/').capitalize()} already exists")

        # Hash the password before saving
        password_service = PasswordService(db)
        hashed_password = password_service.hash(password)

        # Use the appropriate method from the service class to create the new user
        create_method = getattr(svc, create_method_name)
        user = await create_method({"email": email, "password": hashed_password})  # Pass the parsed data with hashed password

        # Generate access and refresh tokens for the newly registered user
        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        # Return the generated tokens in the response
        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
