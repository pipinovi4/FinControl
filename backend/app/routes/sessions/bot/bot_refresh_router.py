from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.db.session import get_async_db
from backend.app.schemas.sessions import TokenPair, RefreshRequest
from backend.app.services.auth import AccessTokenService, RefreshTokenService
from backend.app.permissions.enums import PermissionRole
from backend.app.utils.decorators import handle_route_exceptions
from backend.app.utils.middlewares import rate_limit

# In-memory storage for refresh tokens (can be replaced with a proper cache or database)
bot_tokens = {}

refresh_router = APIRouter(tags=["Refresh"])

def generate_bot_refresh_handler(role: PermissionRole, path: str):
    @handle_route_exceptions
    @rate_limit("10/minute")
    @refresh_router.post(
        path,
        response_model=TokenPair,
        summary=f"Refresh tokens for {role.name.title()}",
        status_code=status.HTTP_200_OK,
        responses={
            200: {"description": "New access and refresh tokens issued"},
            401: {"description": "Invalid or expired refresh token"},
            403: {"description": "Forbidden – wrong role for this endpoint"},
        },
    )
    async def bot_refresh(
        refresh_data: RefreshRequest,  # We now expect the refresh token to come in the request body
        request: Request,
        db: AsyncSession = Depends(get_async_db),
    ) -> TokenPair:
        refresh_svc = RefreshTokenService(db)
        access_svc = AccessTokenService()

        # Verify the provided refresh token
        token_row = await refresh_svc.verify(refresh_data.refresh_token)
        if token_row is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        # Check if the user role matches the expected role
        if token_row.user.role != role:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail=f"Invalid role for this endpoint: expected {role.name}",
            )

        # Generate a new access token and refresh token
        access, ttl = access_svc.create(str(token_row.user_id))
        new_refresh_token = await refresh_svc.rotate(
            stored_token=token_row,
            ip=request.client.host,
            ua=request.headers.get("User-Agent"),
        )

        # Store the new refresh token in bot memory (for simplicity, using a dictionary here)
        bot_tokens[token_row.user_id] = {
            "access_token": access,
            "refresh_token": new_refresh_token,
            "expires_in": ttl
        }

        # Return the new tokens in the response
        return TokenPair(access_token=access, refresh_token=new_refresh_token, expires_in=ttl)
