from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.entities.Client import ClientSchema
from backend.app.services.entities import ClientServices

router = APIRouter()


@router.post(
    "/client",
    summary="Create a new Client",
    response_model=ClientSchema.Out,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Client successfully created"},
        409: {"description": "Client with this Telegram ID already exists"},
        500: {"description": "Internal server error"},
    },
)
def create_client(
    user: ClientSchema.Create,
    db: Session = Depends(get_db),
):
    """
    Create a new client profile.

    - **full_name / phone_number / email**: core contact info
    - **telegram_id & telegram_username**: must be unique
    - **extra finance fields**: amount, assets, etc.
    """
    service = ClientServices(db)

    if service.get_user_by_telegram_id(UUID(user.telegram_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Client with given telegram_id already exists",
        )

    new_client = service.create_client(user)
    return new_client
