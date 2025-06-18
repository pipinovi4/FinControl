from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.app.utils.decorators import handle_route_exceptions
from backend.db.session import get_db
from backend.app.schemas.sessions import TokenPair, RefreshRequest
from backend.app.services.auth import AccessTokenService, RefreshTokenService
from backend.app.permissions.enums import PermissionRole

refresh_router = APIRouter(prefix="/refresh", tags=["Refresh"])

def generate_refresh_handler(role: PermissionRole, path: str):
    @handle_route_exceptions
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
    def refresh(
        payload: RefreshRequest,
        request: Request,
        db: Session = Depends(get_db),
    ) -> TokenPair:
        refresh_svc = RefreshTokenService(db)
        access_svc = AccessTokenService()

        token_row = refresh_svc.verify(payload.refresh_token)
        if token_row is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

        if token_row.user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Invalid role for this endpoint: expected {role.name}")

        access, ttl = access_svc.create(str(token_row.user_id))
        refresh_token = refresh_svc.rotate(
            stored_token=token_row,
            ip=request.client.host,
            ua=request.headers.get("User-Agent"),
        )

        return TokenPair(access_token=access, refresh_token=refresh_token, expires_in=ttl)

# TODO make custom refresh for client because they don't use frontend
# generate_refresh_handler(PermissionRole.CLIENT, "/client")
