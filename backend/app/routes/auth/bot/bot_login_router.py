from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from pydantic import BaseModel

from backend.db.session import get_async_db
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.permissions.enums import PermissionRole
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares import rate_limit

# Define the LoginRequest schema
class LoginRequest(BaseModel):
    login: str  # Can be either email or username
    password: str

login_router = APIRouter(tags=["Login"])

def generate_bot_login_handler(role: PermissionRole, path: str):
    @handle_route_exceptions
    @rate_limit("20/minute")
    @login_router.post(
        path,
        response_model=TokenPair,
        summary=f"{role.name.title()} login and get tokens",
        status_code=status.HTTP_200_OK,
    )
    async def bot_login(
        login_request: LoginRequest,  # Use the LoginRequest schema to parse the request
        request: Request,
        db: AsyncSession = Depends(get_async_db)
    ) -> TokenPair:
        password_service = PasswordService(db)

        # Extract login (email or username) and password from the validated request
        email = login_request.login
        password = login_request.password

        # Check if both email and password are provided
        if not email or not password:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email and password are required")

        # Authenticate the user
        user = await password_service.authenticate(email, password)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # Check if the user role matches the required role
        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not a {role.name.lower()}")

        # Generate tokens
        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent"),
        )

        # Return the generated tokens
        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
