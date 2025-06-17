from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.auth import LoginRequest, TokenPair
from backend.app.services.auth_service import AuthService
from backend.app.permissions.enums import PermissionRole

router = APIRouter()


@router.post(
    "/worker",
    response_model=TokenPair,
    summary="Worker login and get tokens",
    status_code=status.HTTP_200_OK,
)
def worker_login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    auth = AuthService(db)
    user = auth.authenticate(str(credentials.email), credentials.password)
    if not user or user.role != PermissionRole.WORKER:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid worker credentials")

    access, ttl = auth.create_access_token(str(user.id))
    refresh = auth.create_refresh_token(str(user.id), request.client.host, request.headers.get("User-Agent"))
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
