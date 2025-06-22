from __future__ import annotations

from typing import Awaitable, Callable, List, Type
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse

from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import AccessTokenService
from backend.app.services.sessions.refresh_token import RefreshTokenService
from backend.app.utils.cookies import set_auth_cookies
from backend.db.session import get_async_db
from backend.app.routes.sessions._base import generate_refresh_endpoints
from backend.app.routes.sessions.types import RefreshTypes, RefreshRequestT
from backend.app.routes.sessions.config import ROLE_REGISTRY
from backend.app.permissions import PermissionRole

def make_refresh_handler(
    *,
    role: PermissionRole,
    refresh_type: RefreshTypes,
    request_type: RefreshRequestT,
) -> Callable[..., Awaitable]:
    async def _handler(
        request_data: Type[request_type],
        request: Request,
        db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        refresh_svc = RefreshTokenService(db)
        access_svc = AccessTokenService()

        refresh_token: str

        # Determine the refresh token based on refresh_type
        if refresh_type is RefreshTypes.WEB_REFRESH:
            refresh_token = request.cookies.get("refresh_token")
        elif refresh_type is RefreshTypes.BOT_REFRESH:
            refresh_token = request_data.refresh_token
        else:
            # Raise an error if refresh_type is invalid
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid refresh type provided")

        # Verify the refresh token
        token_row = await refresh_svc.verify(refresh_token)

        if token_row is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        if token_row.user.role != role:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail=f"Invalid role for this endpoint: expected {role.name}",
            )

        # Generate new access and refresh tokens
        access, ttl = access_svc.create(str(token_row.user_id))
        refresh = await refresh_svc.rotate(
            stored_token=token_row,
            ip=request.client.host,
            ua=request.headers.get("User-Agent"),
        )

        response: JSONResponse | TokenPair

        # Assign a response variable to return
        if refresh_type is RefreshTypes.WEB_REFRESH:
            response = JSONResponse(content={"access_token": access, "refresh_token": refresh, "expires_in": ttl})
            # Optionally set cookies for web clients
            set_auth_cookies(response, access, refresh, ttl)
        elif refresh_type is RefreshTypes.BOT_REFRESH:
            response = TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid refresh type provided")

        return response # type: ignore

    return _handler

def create_refresh_routers() -> List[APIRouter]:
    routers: List[APIRouter] = []

    for role, (path, refresh_types) in ROLE_REGISTRY.items():
        router: APIRouter = APIRouter()

        for refresh_type, request_type in refresh_types.items():
            handler = make_refresh_handler(
                role=role,
                refresh_type=refresh_type,
                request_type=request_type,
            )

            # Enhanced paths and readable tags
            refresh_path = f"{path}/{refresh_type.name.lower()}"
            tag_name = f"{role.value.lower()}-{refresh_type.name.lower()}"

            generate_refresh_endpoints(
                router=router,
                path=refresh_path,
                handler=handler,
                tags=[tag_name],  # Clean tag for better readability
                rate_limit_rule="10/minute",
                name=f"{role.value.lower()}_{refresh_type.name.lower()}",  # Meaningful handler names
            )

        routers.append(router)

    return routers
