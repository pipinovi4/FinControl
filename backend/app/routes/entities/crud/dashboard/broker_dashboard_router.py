import datetime

from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.schemas.entities.client_schema import ClientBrokerOut, BrokerClientNewToday
from backend.db.session import get_async_db
from app.services.entities.broker.broker_dashboard import BrokerDashboard
from app.services.entities.credit.credit_service import CreditService, CreditStatus
from app.schemas.entities.credit_schema import (
    CreditOut, CreditStatusUpdate, CreditCommentIn, BrokerPaginatedCreditsOut
)
from app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    BrokerClientListOut,
    BrokerIdIn,
    BrokerSignClientIn,
    StatusMessage,
    ClientIdIn,
    BrokerBucketClientsIn, BrokerCreateCredit, SimpleFloatOut,
)

router = APIRouter(
    prefix="/client",
    tags=["broker:dashboard"]
)

# 1. Total number of all credits from broker's clients
@router.get("/credits/count/total/{broker_id}", response_model=SimpleIntOut)
async def get_total_credits_count(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_total_credits_count(broker_id)
    return SimpleIntOut(value=count)
get_total_credits_count._meta = {"input_model": BrokerIdIn}


# 2. Credits issued this month
@router.get("/credits/count/month/{broker_id}", response_model=SimpleIntOut)
async def get_month_credits_count(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_mount_credits_count(broker_id)
    return SimpleIntOut(value=count)
get_month_credits_count._meta = {"input_model": BrokerIdIn}

# 3. Active credits
@router.get("/credits/count/active/{broker_id}", response_model=SimpleIntOut)
async def get_active_credits_count(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_count_active_credits(broker_id)
    return SimpleIntOut(value=count)
get_active_credits_count._meta = {"input_model": BrokerIdIn}

# 4. Completed credits
@router.get("/credits/count/completed/{broker_id}", response_model=SimpleIntOut)
async def get_completed_credits_count(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_count_completed_credits(broker_id)
    return SimpleIntOut(value=count)
get_completed_credits_count._meta = {"input_model": BrokerIdIn}

# 5. Signed clients (attached to workers)
@router.get("/signed/sum/{broker_id}", response_model=SimpleIntOut)
async def get_sum_signed_clients(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_signed_clients(broker_id)
    return SimpleIntOut(value=count)
get_sum_signed_clients._meta = {"input_model": BrokerIdIn}

# 6. Paginated signed clients
@router.get("/signed/bucket/{broker_id}", response_model=BrokerClientListOut)
async def get_signed_clients(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1),
    db: AsyncSession = Depends(get_async_db)
):
    service = BrokerDashboard(db)
    signed_clients = await service.get_bucket_signed_clients(broker_id, skip=skip, limit=limit)
    total = await service.get_sum_signed_clients(broker_id)
    return {
        "clients": [ClientBrokerOut.model_validate(c) for c in signed_clients],
        "total": total
    }
get_signed_clients._meta = {"input_model": BrokerBucketClientsIn}

# 7. Paginated unsigned clients
@router.get("/unsigned/{broker_id}", response_model=BrokerClientListOut)
async def get_unsigned_clients(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1),
    db: AsyncSession = Depends(get_async_db)
):
    service = BrokerDashboard(db)
    return await service.get_bucket_unsigned_clients(broker_id, skip=skip, limit=limit)
get_unsigned_clients._meta = {"input_model": BrokerBucketClientsIn}

# 8. Get single client info
@router.get("/{client_id}", response_model=ClientBrokerOut)
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    client = await service.get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return ClientBrokerOut.model_validate(client)
get_client._meta = {"input_model": ClientIdIn}

# 9. Sign client to a worker
@router.patch("/sign", response_model=StatusMessage)
async def sign_client(data: BrokerSignClientIn, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    await service.sign_client(data.client_id, data.broker_id)
    return {"status": "client signed"}
sign_client._meta = {"input_model": BrokerSignClientIn}

# 10. Unsign client
@router.patch("/unsign/{client_id}", response_model=StatusMessage)
async def unsign_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    await service.unsign_client(client_id)
    return {"status": "client unsigned"}
unsign_client._meta = {"input_model": ClientIdIn}

#11. Create credit
@router.post("/create-credit", response_model=StatusMessage)
async def create_credit(data: BrokerCreateCredit, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    await service.create_credit(data.client_id, data.broker_id, data.amount)
    return {"status": "credit created"}
create_credit._meta = {"input_model": BrokerCreateCredit}

# 12. Count new clients taken today
@router.get("/new-today/sum/{broker_id}", response_model=SimpleIntOut)
async def get_sum_today_new_clients(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    total = await service.get_sum_today_new_clients(broker_id)
    return SimpleIntOut(value=total)
get_sum_today_new_clients._meta = {"input_model": BrokerIdIn}

# 13. Count new clients taken yesterday
@router.get("/new-yesterday/sum/{broker_id}", response_model=SimpleIntOut)
async def get_sum_yesterday_new_clients(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    total = await service.get_sum_yesterday_new_clients(broker_id)
    return SimpleIntOut(value=total)
get_sum_yesterday_new_clients._meta = {"input_model": BrokerIdIn}

# 14. New clients taken today by broker
@router.get("/new-today/{broker_id}", response_model=list[BrokerClientNewToday])
async def get_today_new_clients(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    return await service.get_today_new_clients(broker_id)
get_today_new_clients._meta = {"input_model": BrokerIdIn}

# 15. Total sum of all credits from broker's clients
@router.get("/credits/sum/total/{broker_id}", response_model=SimpleIntOut)
async def get_total_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    commissions_sum = await service.get_sum_broker_commissions(broker_id)
    return SimpleFloatOut(value=commissions_sum)
get_total_credits_sum._meta = {"input_model": BrokerIdIn}


# 16. Credits issued this month
@router.get("/credits/sum/month/{broker_id}", response_model=SimpleIntOut)
async def get_month_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    commissions_sum = await service.get_month_broker_commissions(broker_id)
    return SimpleFloatOut(value=commissions_sum)
get_month_credits_sum._meta = {"input_model": BrokerIdIn}

# 17. Active credits
@router.get("/credits/sum/active/{broker_id}", response_model=SimpleFloatOut)
async def get_active_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_active_credits(broker_id)
    return SimpleFloatOut(value=count)
get_active_credits_sum._meta = {"input_model": BrokerIdIn}

# 18. Completed credits
@router.get("/credits/sum/completed/{broker_id}", response_model=SimpleFloatOut)
async def get_completed_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_completed_credits(broker_id)
    return SimpleFloatOut(value=count)
get_completed_credits_sum._meta = {"input_model": BrokerIdIn}

# 19. Get credits for month
@router.get("/credits/sum/monthly/{broker_id}")
async def get_credits_for_month(
    broker_id: UUID,
    month: str = Query(..., example="2025-06"),
    db: AsyncSession = Depends(get_async_db)
):
    service = BrokerDashboard(db)
    total = await service.get_credits_for_month(broker_id, month)
    return {"value": total}

# 20. Get credits for year
@router.get("/credits/sum/yearly/{broker_id}")
async def get_credits_for_year(
    broker_id: UUID,
    year: int = Query(..., example=2025),
    db: AsyncSession = Depends(get_async_db)
):
    service = BrokerDashboard(db)
    data = await service.get_credits_for_year(broker_id, year)
    return {"items": data}

# 16. Get client by filters
@router.get(
    "/filter/bucket/{broker_id}",
    response_model=BrokerClientListOut,
    summary="Пагинированный список клиентов c фильтрами"
)
async def filter_bucket_clients_of_worker(
    broker_id: UUID,
    skip: int  = Query(0,  ge=0,  description="Сколько записей пропустить"),
    limit: int = Query(6,  ge=1,  le=100, description="Сколько вернуть"),
    email: str | None        = Query(None, description="Часть e-mail"),
    phone_number: str | None = Query(None, description="Часть номера"),
    full_name: str | None    = Query(None, description="Часть ФИО"),
    db: AsyncSession = Depends(get_async_db),
):
    service = BrokerDashboard(db)

    clients, total = await service.filter_bucket_clients(
        broker_id=broker_id,
        skip=skip,
        limit=limit,
        email=email,
        phone_number=phone_number,
        full_name=full_name,
    )

    return {"clients": clients, "total": total}

# ───────────────────────────────────────────────
# BROKER: CREDITS (view & limited updates)
# ───────────────────────────────────────────────

@router.get("/credits/{broker_id}", response_model=BrokerPaginatedCreditsOut)
async def broker_list_credits(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    statuses: Optional[List[CreditStatus]] = Query(None),
    client_id: Optional[UUID] = Query(None),
    created_from: Optional[datetime.datetime] = Query(default=None),
    created_to: Optional[datetime.datetime] = Query(default=None),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Брокер бачить лише СВОЇ кредити. Фільтри та пагінація.
    """
    service = CreditService(db)
    items, total = await service.list_for_broker_paginated(
        broker_id,
        skip=skip,
        limit=limit,
        statuses=statuses,
        client_id=client_id,
        created_from=created_from,
        created_to=created_to,
    )
    return BrokerPaginatedCreditsOut(
        credits=[CreditOut.model_validate(c) for c in items],
        total=total,
    )


@router.get("/credits/{broker_id}/{credit_id}", response_model=CreditOut)
async def broker_get_credit(
    broker_id: UUID,
    credit_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Брокер може отримати тільки кредит, який прив’язаний до нього.
    """
    service = CreditService(db)
    credit = await service.get_for_broker(credit_id, broker_id)
    return CreditOut.model_validate(credit)


@router.patch("/credits/{broker_id}/{credit_id}/status", response_model=CreditOut)
async def broker_change_status(
    broker_id: UUID,
    credit_id: UUID,
    payload: CreditStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Дозволені значення для брокера: APPROVED / TREATMENT / REJECTED.
    """
    service = CreditService(db)

    # перевірка доступу
    await service.get_for_broker(credit_id, broker_id)

    updated = await service.broker_update_status(credit_id, payload.status)
    return CreditOut.model_validate(updated)


@router.post("/credits/{broker_id}/{credit_id}/comment", response_model=CreditOut)
async def broker_add_comment(
    broker_id: UUID,
    credit_id: UUID,
    comment: CreditCommentIn,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Брокер залишає коментар (наприклад для статусу TREATMENT).
    """
    service = CreditService(db)

    # перевірка доступу
    await service.get_for_broker(credit_id, broker_id)

    updated = await service.add_comment(credit_id, comment.text)
    return CreditOut.model_validate(updated)
