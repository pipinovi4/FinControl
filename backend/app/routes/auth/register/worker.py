from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.auth import TokenPair
from backend.app.schemas.entities.Worker import WorkerSchema
from backend.app.services.entities import WorkerService
from backend.app.services.auth_service import AuthService

router = APIRouter(prefix="/auth/register", tags=["Authentication"])


@router.post(
    "/worker",
    response_model=TokenPair,
    summary="Register a new Worker and get tokens",
    status_code=status.HTTP_201_CREATED,
)
def register_worker(
    payload: WorkerSchema.Create,
    request: Request,
    db: Session = Depends(get_db),
):
    svc = WorkerService(db)

    if svc.get_user_by_telegram_id(UUID(payload.telegram_id)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Worker already exists")

    worker = svc.create_worker(payload)

    auth = AuthService(db)
    access, ttl = auth.create_access_token(str(worker.id))
    refresh = auth.create_refresh_token(str(worker.id), request.client.host, request.headers.get("User-Agent"))

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
