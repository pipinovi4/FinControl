from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.db.session import get_async_db
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.permissions.enums import PermissionRole
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares import rate_limit

login_router = APIRouter(tags=["Login"])

def generate_login_handler(role: PermissionRole, path: str):
    @handle_route_exceptions
    @rate_limit("20/minute")
    @login_router.post(
        path,
        response_model=TokenPair,
        summary=f"{role.name.title()} login and get tokens",
        status_code=status.HTTP_200_OK,
    )
    async def login(
        credentials: LoginRequest,
        request: Request,
        db: AsyncSession = Depends(get_async_db),
        response: Response = Depends()
    ) -> TokenPair:
        password_service = PasswordService(db)
        user = await password_service.authenticate(str(credentials.email), credentials.password)

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

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,  #
            samesite="strict",
            expires=ttl
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="strict",
            expires=ttl
        )

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
