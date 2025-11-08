# backend/app/routes/auth/invite.py
from fastapi import APIRouter, Depends, Body, status, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.permissions import PermissionRole
from app.schemas.auth.invite_schema import InviteInfoOut
from app.utils.cookies import set_auth_cookies

from app.schemas import WorkerSchema, BrokerSchema
from app.services.auth import generate_token_pair
from app.services.entities import WorkerService, BrokerService
from app.services.auth.invite_service import InviteService
from db.session import get_async_db

router = APIRouter(prefix="/invite", tags=["Auth"])

@router.get("/meta/{token}", response_model=InviteInfoOut)
async def invite_meta(token: str, db=Depends(get_async_db)):
    invite = await InviteService(db).peek_invite(token)
    return InviteInfoOut(role=invite.role, expires_at=invite.expires_at)

@router.post("/worker/{token}", status_code=status.HTTP_201_CREATED, response_model=WorkerSchema.WebRegisterResponse)
async def worker_invite_register(
    token: str,
    request: Request,
    data: WorkerSchema.Create = Body(...),
    db=Depends(get_async_db),
):
    service = InviteService(db)
    worker_service = WorkerService(db)

    invite = await service.peek_invite(token)

    if invite.role != PermissionRole.WORKER:
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Токен не является действительным для Worker')
    if await worker_service.get_by_email(data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, detail="User already exists")

    worker = await worker_service.create(WorkerSchema.Create(**data.model_dump()))

    worker = await worker_service.get_by_id(worker.id)

    await service.consume_invite(invite)

    access, refresh, expires_in = await generate_token_pair(
        worker.id, db, request.client.host, request.headers.get("User-Agent")
    )

    response = JSONResponse(content=jsonable_encoder(WorkerSchema.WebRegisterResponse.model_validate(worker)))
    set_auth_cookies(response, access, refresh, expires_in)
    return response

@router.post("/broker/{token}", status_code=status.HTTP_201_CREATED, response_model=BrokerSchema.WebRegisterResponse)
async def broker_invite_register(
    token: str,
    request: Request,
    data: BrokerSchema.Create = Body(...),
    db=Depends(get_async_db),
):
    service = InviteService(db)
    broker_service = BrokerService(db)

    # 1) перевіряємо токен, але НЕ зжираємо
    invite = await service.peek_invite(token)

    if invite.role != PermissionRole.BROKER :
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Токен не является действительным для Broker')

    # 2) створюємо користувача
    broker = await broker_service.create(BrokerSchema.Create(**data.model_dump()))

    broker = await broker_service.get_by_id(broker.id)

    # 3) тепер можемо з'їсти інвайт
    await service.consume_invite(invite)

    access, refresh, expires_in = await generate_token_pair(
        broker.id, db, request.client.host, request.headers.get("User-Agent")
    )
    response = JSONResponse(content=jsonable_encoder(BrokerSchema.WebRegisterResponse.model_validate(broker)))
    set_auth_cookies(response, access, refresh, expires_in)
    return response