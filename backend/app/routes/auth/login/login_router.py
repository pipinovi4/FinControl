from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.utils.cookies import set_auth_cookies
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
        db: AsyncSession = Depends(get_async_db)
    ) -> JSONResponse:
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

        response = JSONResponse(content={"access_token": access, "refresh_token": refresh, "expires_in": ttl})

        set_auth_cookies(response, access, refresh, ttl)

        return response
