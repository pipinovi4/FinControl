from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.services.auth import generate_token_pair
from backend.db.session import get_db
from backend.app.schemas.auth import TokenPair
from backend.app.schemas.entities.Worker import WorkerSchema
from backend.app.services.entities import WorkerService

router = APIRouter()


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

    if svc.get_user_by_telegram_id(payload.telegram_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Worker already exists")

    worker = svc.create_worker(payload)

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(worker.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
