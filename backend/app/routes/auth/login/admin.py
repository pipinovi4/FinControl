from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.auth import LoginRequest, TokenPair
from backend.app.services.auth_service import AuthService
from backend.app.permissions.enums import PermissionRole

router = APIRouter()


@router.post("/admin", response_model=TokenPair, summary="Admin login and get tokens")
def admin_login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    auth = AuthService(db)
    user = auth.authenticate(str(credentials.email), credentials.password)

    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if user.role != PermissionRole.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not an admin")

    access, ttl = auth.create_access_token(str(user.id))
    refresh = auth.create_refresh_token(str(user.id), request.client.host, request.headers.get("User-Agent"))

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
