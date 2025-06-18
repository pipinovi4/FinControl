from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.auth import TokenPair
from backend.app.schemas.entities.Admin import AdminSchema
from backend.app.services.entities import AdminService
from backend.app.services.auth import generate_token_pair

router = APIRouter()

@router.post(
    "/admin",
    response_model=TokenPair,
    summary="Register a new Admin and get tokens",
    status_code=status.HTTP_201_CREATED,
)
def register_admin(
    payload: AdminSchema.Create,
    request: Request,
    db: Session = Depends(get_db),
):
    svc = AdminService(db)

    if svc.get_user_by_telegram_id(payload.telegram_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Admin already exists")

    admin = svc.create_admin(payload)

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(admin.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
