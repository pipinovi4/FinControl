from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
import secrets
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.auth import TokenPair
from backend.app.schemas.entities.Broker import BrokerSchema
from backend.app.services.entities import BrokerService
from backend.app.services.auth import generate_token_pair

router = APIRouter()


@router.post(
    "/broker",
    response_model=TokenPair,
    summary="Register a new Broker and get tokens",
    status_code=status.HTTP_201_CREATED,
)
def register_broker(
    payload: BrokerSchema.Create,
    request: Request,
    db: Session = Depends(get_db),
):
    svc = BrokerService(db)

    if svc.get_user_by_telegram_id(payload.telegram_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Broker already exists")

    broker = svc.create_broker(payload)

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(broker.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
