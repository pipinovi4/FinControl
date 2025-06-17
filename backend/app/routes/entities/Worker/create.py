from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.entities.Worker import WorkerSchema
from backend.app.services.entities import WorkerService

router = APIRouter()


@router.post(
    "/client",
    summary="Create a new Worker",
    response_model=WorkerSchema.Out,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Worker successfully created"},
        409: {"description": "Worker with this Telegram ID already exists"},
        500: {"description": "Internal server error"},
    },
)
def create_worker(
    user: WorkerSchema.Create,
    db: Session = Depends(get_db),
):
    """
    Create a new internal worker.

    - **email / username**: unique credentials
    - **telegram_id & telegram_username**: unique Telegram identifiers
    - **password_hash**: optional if dynamic-link auth used
    """
    service = WorkerService(db)

    if service.get_user_by_telegram_id(user.telegram_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Worker with given telegram_id already exists",
        )

    new_worker = service.create_worker(user)
    return new_worker
