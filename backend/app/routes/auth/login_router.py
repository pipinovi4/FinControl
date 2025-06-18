from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.sessions import TokenPair
from backend.app.services.auth import PasswordService, generate_token_pair
from backend.app.permissions.enums import PermissionRole
from backend.app.utils.decorators import handle_route_exceptions

login_router = APIRouter()


def generate_login_handler(role: PermissionRole, path: str):
    @handle_route_exceptions
    @login_router.post(
        path,
        response_model=TokenPair,
        summary=f"{role.name.title()} login and get tokens",
        status_code=status.HTTP_200_OK,
    )
    def login(
        credentials: LoginRequest,
        request: Request,
        db: Session = Depends(get_db),
    ) -> TokenPair:
        password_service = PasswordService(db)
        user = password_service.authenticate(str(credentials.email), credentials.password)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not a {role.name.lower()}")

        access, refresh, ttl = generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent"),
        )

        return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
