from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.permissions.enums import PermissionRole
from backend.app.utils.decorators import handle_route_exceptions

router = APIRouter()


@handle_route_exceptions
@router.post(
    "/client",
    response_model=TokenPair,
    summary="Client login and get tokens",
    status_code=status.HTTP_200_OK,
)
def client_login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    password_service = PasswordService(db)
    client = password_service.authenticate(str(credentials.email), credentials.password)

    if client is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if client.role != PermissionRole.CLIENT:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not a client")

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(client.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
