from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Type, Any, TypeVar

from backend.app.schemas import AdminSchema, WorkerSchema, BrokerSchema, ClientSchema
from backend.app.services.entities import AdminService, WorkerService, BrokerService, ClientServices
from backend.db.session import get_db
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
    ClientServices
)

def generate_register_handler(
    path: str,
    service_class: Type[ServiceT],
    schema_class: Type[SchemaT],
    create_method_name: str,
):
    @handle_route_exceptions
    @register_router.post(
        path,
        response_model=TokenPair,
        summary=f"Register a new {path.strip('/').capitalize()} and get tokens",
        status_code=status.HTTP_201_CREATED,
    )
    def register(
        payload: SchemaT,
        request: Request,
        db: Session = Depends(get_db),
    ) -> TokenPair:
        svc = service_class(db)

        if svc.get_user_by_telegram_id(payload.telegram_id):
            raise HTTPException(status.HTTP_409_CONFLICT, f"{path.strip('/').capitalize()} already exists")

        create_method = getattr(svc, create_method_name)
        user = create_method(payload)

        access, refresh, ttl = generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
