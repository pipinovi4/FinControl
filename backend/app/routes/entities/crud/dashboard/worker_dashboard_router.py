from fastapi import APIRouter, Depends

from backend.app.schemas.entities.earning_schema import EarningCreate, EarningCreateIn
from backend.db.session import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.services.entities.worker.worker_dashboard import WorkerDashboardService
from backend.app.schemas.entities.client_schema import ClientOut
from backend.app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    SimpleFloatOut,
    WorkerClientListOut,
    ClientIdIn,
    WorkerIdIn,
    WorkerBucketClientsIn, WorkerSignClientIn, StatusMessage,
)

router = APIRouter(
    prefix="/client",
    tags=["worker:dashboard"]
)

# 1. Total number of clients
@router.get("/sum/{worker_id}", response_model=SimpleIntOut)
async def get_clients_sum(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_clients(worker_id)}
get_clients_sum._meta = {"input_model": WorkerIdIn}


# 2. Total earnings
@router.get("/earnings/total/{worker_id}", response_model=SimpleFloatOut)
async def get_total_earnings(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_total_sum_earnings(worker_id)}
get_total_earnings._meta = {"input_model": WorkerIdIn}


# 3. Monthly earnings
@router.get("/earnings/month/{worker_id}", response_model=SimpleFloatOut)
async def get_month_earnings(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_month_sum_earnings(worker_id)}
get_month_earnings._meta = {"input_model": WorkerIdIn}


# 4. Total number of deals (earnings entries)
@router.get("/deals-sum/{worker_id}", response_model=SimpleIntOut)
async def get_sum_deals(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_deals(worker_id)}
get_sum_deals._meta = {"input_model": WorkerIdIn}


# 5. Today's new clients
@router.get("/new-today/{worker_id}", response_model=SimpleIntOut)
async def get_sum_today_new_clients(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_today_new_clients(worker_id)}
get_sum_today_new_clients._meta = {"input_model": WorkerIdIn}


# 6. Paginated clients list
@router.get("/bucket/{worker_id}", response_model=WorkerClientListOut)
async def get_bucket_clients(
    worker_id: UUID,
    skip: int = 0,
    limit: int = 8,
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    clients = await service.get_bucket_clients(worker_id, skip=skip, limit=limit)
    return {"clients": clients, "total": len(clients)}
get_bucket_clients._meta = {"input_model": WorkerBucketClientsIn}


# 7. Get client by ID
@router.get("/{client_id}", response_model=ClientOut)
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return await service.get_client(client_id)
get_client._meta = {"input_model": ClientIdIn}


# 8. Unassign a client from a worker
@router.patch("/unsign/{client_id}", response_model=StatusMessage)
async def unsign_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.unsign_client(client_id)
    return {"status": "client unsigned"}
unsign_client._meta = {"input_model": ClientIdIn}


# 9. Assign client to worker
@router.patch("/sign", response_model=StatusMessage)
async def sign_client(data: WorkerSignClientIn, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.sign_client(data.client_id, data.worker_id)
    return {"status": "client signed"}
sign_client._meta = {"input_model": WorkerSignClientIn}

# 10. Create new earning
@router.post("/create-earning", response_model=StatusMessage)
async def create_earning(
    payload: EarningCreateIn,
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    await service.create_new_earning(payload.client_id, payload.worker_id, payload.amount)
    return {"status": "earning created"}
create_earning._meta = {"input_model": EarningCreateIn}

# 26458bfc-f6c9-450b-8839-a196572a24c4