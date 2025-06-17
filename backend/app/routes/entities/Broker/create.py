from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.app.schemas.entities.Broker import BrokerSchema
from backend.app.services.entities import BrokerService

router = APIRouter()


@router.post(
    "/broker",
    summary="Create a new Broker",
    response_model=BrokerSchema.Out,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Broker successfully created"},
        409: {"description": "Broker with this Telegram ID already exists"},
        500: {"description": "Internal server error"},
    },
)
def create_broker(
    user: BrokerSchema.Create,
    db: Session = Depends(get_db),
):
    """
    Create a new broker user.

    - **email**: login e-mail, must be unique
    - **telegram_id**: unique Telegram ID
    - **telegram_username**: Telegram handle
    - **company_name / region**: optional business info
    """
    service = BrokerService(db)

    if service.get_user_by_telegram_id(UUID(user.telegram_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Broker with given telegram_id already exists",
        )

    new_broker = service.create_broker(user)
    return new_broker
