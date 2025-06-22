from __future__ import annotations

from typing import Awaitable, Callable, List, Type
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from uuid import UUID

from backend.app.routes.auth.login.types import LoginTypes
from backend.app.routes.auth.login.config import ROLE_REGISTRY
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.utils.cookies import set_auth_cookies
from backend.db.session import get_async_db
from backend.app.routes.auth.login._base import generate_login_endpoints
from backend.app.permissions import PermissionRole

def make_login_handler(
        role: PermissionRole,
        login_type: LoginTypes,
) -> Callable[..., Awaitable]:
    async def _handler(
        request_data: LoginRequest,
        request: Request,
        db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        password_service = PasswordService(db)
        user = await password_service.authenticate(str(request_data.email), request_data.password)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not a {role.name.lower()}")

        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent"),
        )

        response: JSONResponse | TokenPair

        if LoginTypes.WEB in login_type:
            response = JSONResponse(content={"access_token": access, "refresh_token": refresh, "expires_in": ttl})
            set_auth_cookies(response, access, refresh, ttl)
        elif LoginTypes.BOT in login_type:
            return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid login type provided")

        return response

    return _handler

def create_login_routers() -> List[APIRouter]:
    routers: List[APIRouter] = []

    for role, (path, login_types) in ROLE_REGISTRY.items():
        router: APIRouter = APIRouter()

        for login_type in login_types:
            handler = make_login_handler(
                role=role,
                login_type=login_type,
            )

            # Enhanced paths and readable tags
            login_path = f"{path}/{login_type.name.lower()}"
            tag_name = f"{role.value.lower()}-{login_type.name.lower()}"

            generate_login_endpoints(
                router=router,
                path=login_path,
                handler=handler,
                tags=[tag_name],  # Clean tag for better readability
                rate_limit_rule="10/minute",
                name=f"login_{role.value.lower()}_{login_type.name.lower()}",  # Meaningful handler names
            )

        routers.append(router)

    return routers

# TODO need to make condition for check LoginType and pass to generate_token_pair not headers