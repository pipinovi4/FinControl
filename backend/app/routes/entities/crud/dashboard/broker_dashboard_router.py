from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.db.session import get_async_db
from backend.app.services.entities.broker.broker_dashboard import BrokerDashboard
from backend.app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    BrokerClientListOut,
    ClientOut,
    BrokerIdIn,
    BrokerSignClientIn,
    StatusMessage,
    ClientIdIn,
    BrokerBucketClientsIn, BrokerCreateCredit,
)

router = APIRouter(
    prefix="/client",
    tags=["broker:dashboard"]
)

# 1. Total number of all credits from broker's clients
@router.get("/credits/sum/{broker_id}", response_model=SimpleIntOut)
async def get_total_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_total_credits_sum(broker_id)
    return SimpleIntOut(value=count)
get_total_credits_sum._meta = {"input_model": BrokerIdIn}


# 2. Credits issued this month
@router.get("/credits/month/{broker_id}", response_model=SimpleIntOut)
async def get_mount_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_mount_credits_sum(broker_id)
    return SimpleIntOut(value=count)
get_mount_credits_sum._meta = {"input_model": BrokerIdIn}

# 3. Active credits
@router.get("/credits/active/{broker_id}", response_model=SimpleIntOut)
async def get_active_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_active_credits(broker_id)
    return SimpleIntOut(value=count)
get_active_credits_sum._meta = {"input_model": BrokerIdIn}

# 4. Completed credits
@router.get("/credits/completed/{broker_id}", response_model=SimpleIntOut)
async def get_completed_credits_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_completed_credits(broker_id)
    return SimpleIntOut(value=count)
get_completed_credits_sum._meta = {"input_model": BrokerIdIn}

# 5. Signed clients (attached to workers)
@router.get("/signed/sum/{broker_id}", response_model=SimpleIntOut)
async def get_sum_signed_clients(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    count = await service.get_sum_signed_clients(broker_id)
    return SimpleIntOut(value=count)
get_sum_signed_clients._meta = {"input_model": BrokerIdIn}

# 6. Paginated signed clients
@router.get("/signed/{broker_id}", response_model=BrokerClientListOut)
async def get_signed_clients(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1),
    db: AsyncSession = Depends(get_async_db)
):
    service = BrokerDashboard(db)
    return await service.get_bucket_signed_clients(broker_id, skip=skip, limit=limit)
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
@router.get("/{client_id}", response_model=ClientOut)
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    return await service.get_client(client_id)
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
async def unsign_client(data: BrokerCreateCredit, db: AsyncSession = Depends(get_async_db)):
    service = BrokerDashboard(db)
    await service.create_credit(data.client_id, data.broker_id, data.amount)
    return {"status": "credit created"}
unsign_client._meta = {"input_model": BrokerCreateCredit}
