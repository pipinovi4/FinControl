from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from backend.app.services.auth import generate_token_pair
from backend.db.session import get_db
from backend.app.schemas.auth import TokenPair
from backend.app.schemas.entities.Client import ClientSchema
from backend.app.services.entities import ClientServices

router = APIRouter()


@router.post(
    "/client",
    response_model=TokenPair,
    summary="Register a new Client and get tokens",
    status_code=status.HTTP_201_CREATED,
)
def register_client(
    payload: ClientSchema.Create,
    request: Request,
    db: Session = Depends(get_db),
):
    svc = ClientServices(db)

    if svc.get_user_by_telegram_id(payload.telegram_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Client already exists")

    client = svc.create_client(payload)

    access, refresh, ttl = (
        generate_token_pair(
            UUID(str(client.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent")
        )
    )

    return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
