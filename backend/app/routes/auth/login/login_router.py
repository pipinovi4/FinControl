# backend/app/routes/auth/login/router.py
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast

from db.session              import get_async_db
from app.models.entities     import User            # ← Base class
from app.permissions import PermissionRole
from app.schemas import AdminSchema, BrokerSchema, WorkerSchema, ClientSchema
from app.schemas.sessions    import TokenPair
from app.services.auth       import (
    PasswordService,
    generate_token_pair,
)
from app.utils.cookies       import set_auth_cookies
from app.utils.decorators    import handle_route_exceptions
from app.utils.middlewares.limiter import rate_limit   # якщо треба

router = APIRouter(tags=["Auth"])


RESPONSE_MODELS = {
    PermissionRole.ADMIN: AdminSchema.WebRegisterResponse,
    PermissionRole.BROKER: BrokerSchema.WebRegisterResponse,
    PermissionRole.WORKER: WorkerSchema.WebRegisterResponse,
}



# ──────────────────────────────  SCHEMAS  ──────────────────────────────
class LoginRequest(BaseModel):
    email:    EmailStr
    password: str

WEB_RL = "10/minute"      # <- або прибери, якщо не потрібен rate-limit

from app.services.entities import AdminService, BrokerService, WorkerService, ClientService

async def get_full_user_data(role: PermissionRole, user_id: UUID, db: AsyncSession) -> dict:
    match role:
        case PermissionRole.ADMIN:
            admin = await AdminService(db).get_by_id(user_id)
            return AdminSchema.WebRegisterResponse.model_validate(admin).model_dump()
        case PermissionRole.BROKER:
            broker = await BrokerService(db).get_by_id(user_id)
            return BrokerSchema.WebRegisterResponse.model_validate(broker).model_dump()
        case PermissionRole.WORKER:
            worker = await WorkerService(db).get_by_id(user_id)
            return WorkerSchema.WebRegisterResponse.model_validate(worker).model_dump()
        case PermissionRole.CLIENT:
            client = await ClientService(db).get_by_id(user_id)
            return ClientSchema.Out.model_dump(client).model_dump()

# ──────────────────────────────  HANDLERS  ─────────────────────────────
@router.post(
    "/web",
    response_model=AdminSchema.WebRegisterResponse | BrokerSchema.WebRegisterResponse | WorkerSchema.WebRegisterResponse,
    name="login_web",
    summary="Login (web, cookie-based)",
)
@handle_route_exceptions()
async def login_web(
    request: Request,
    payload: LoginRequest = Body(...),
    db: AsyncSession = Depends(get_async_db),
) -> ORJSONResponse:
    svc = PasswordService(db)
    user: User | None = await svc.authenticate(cast(str, payload.email), payload.password)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate token pair
    access, refresh, ttl = await generate_token_pair(
        user.id, db, request.client.host, request.headers.get("User-Agent")
    )

    # Fetch full user info
    full_user_data = await get_full_user_data(user.role, user.id, db)

    # Dynamically choose the response schema
    schema_cls = RESPONSE_MODELS.get(user.role)
    if not schema_cls:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown role")

    # Prepare response
    response_data = schema_cls(**full_user_data)
    resp = ORJSONResponse(content=response_data.model_dump(mode="json"))
    set_auth_cookies(resp, access, refresh, ttl)
    return resp


@router.post(
    "/bot",
    response_model=TokenPair,
    name="login_bot",
    summary="Login for bots (returns plain JWT pair)",
)
@handle_route_exceptions()
async def login_bot(
    request: Request,
    payload: LoginRequest = Body(...),
    db: AsyncSession = Depends(get_async_db),
) -> TokenPair:
    """
    Те саме, але **без** cookie — віддаємо пару токенів у JSON.
    """
    svc = PasswordService(db)
    user: User | None = await svc.authenticate(cast(str, payload.email), payload.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access, refresh, ttl = await generate_token_pair(
        user.id, db, request.client.host, request.headers.get("User-Agent")
    )
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
