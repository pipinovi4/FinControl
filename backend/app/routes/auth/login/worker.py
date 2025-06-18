from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.auth import LoginRequest, TokenPair
from backend.app.services.auth import AccessTokenService, RefreshTokenService, PasswordService, generate_token_pair
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
    password_service = PasswordService(db)
    worker = password_service.authenticate(str(credentials.email), credentials.password)

    if worker is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if worker.role != PermissionRole.WORKER:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a worker")

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(worker.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
