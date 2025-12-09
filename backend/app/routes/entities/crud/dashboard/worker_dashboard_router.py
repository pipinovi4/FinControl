from fastapi import APIRouter, Depends

from db.session import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.services.entities.worker.worker_dashboard import WorkerDashboardService
from app.schemas.entities.application_schema import ClientOut, WorkerClientNewToday, ClientWorkerOut
from app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    SimpleFloatOut,
    WorkerClientListOut,
    ClientIdIn,
    WorkerIdIn,
    WorkerBucketClientsIn, WorkerSignClientIn, StatusMessage,
)

router = APIRouter(
    prefix="/application",
    tags=["worker:dashboard"]
)

# 1. Total number of clients
@router.get("/sum/{worker_id}", response_model=SimpleIntOut)
async def get_clients_sum(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_clients(worker_id)}
get_clients_sum._meta = {"input_model": WorkerIdIn}


# 2. Total credits
@router.get("/credits/total/{worker_id}", response_model=SimpleFloatOut)
async def get_total_credits(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_total_sum_credits(worker_id)}
get_total_credits._meta = {"input_model": WorkerIdIn}


# 3. Monthly credits
@router.get("/credits/month/{worker_id}", response_model=SimpleFloatOut)
async def get_month_credits(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_month_sum_credits(worker_id)}
get_month_credits._meta = {"input_model": WorkerIdIn}


# 4. Total number of deals (credits entries)
@router.get("/deals-sum/{worker_id}", response_model=SimpleIntOut)
async def get_sum_deals(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_deals(worker_id)}
get_sum_deals._meta = {"input_model": WorkerIdIn}


# 5. Today's new clients count
@router.get("/new-today/count/{worker_id}", response_model=SimpleIntOut)
async def get_sum_today_new_clients(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_today_new_clients(worker_id)}
get_sum_today_new_clients._meta = {"input_model": WorkerIdIn}

# 5. Today's new clients count
@router.get("/yesterday-today/count/{worker_id}", response_model=SimpleIntOut)
async def get_sum_yesterday_new_clients(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_yesterday_new_clients(worker_id)}
get_sum_today_new_clients._meta = {"input_model": WorkerIdIn}

# 6. Today's new clients
@router.get("/new-today/{worker_id}", response_model=list[WorkerClientNewToday])
async def get_sum_today_new_clients(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return await service.get_today_new_clients(worker_id)
get_sum_today_new_clients._meta = {"input_model": WorkerIdIn}

# 7. Paginated signed clients list
@router.get("/bucket/{worker_id}", response_model=WorkerClientListOut)
async def get_bucket_clients(
    worker_id: UUID,
    skip: int = 0,
    limit: int = 6,
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    clients = await service.get_bucket_clients(worker_id, skip=skip, limit=limit)
    total_clients = await service.get_sum_clients(worker_id)
    return {"clients": clients, "total": total_clients}
get_bucket_clients._meta = {"input_model": WorkerBucketClientsIn}

# 8. Get application by ID
@router.get("/{client_id}", response_model=ClientWorkerOut)
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return await service.get_client(client_id)
get_client._meta = {"input_model": ClientIdIn}


# 9. Unassign a application from a worker
@router.patch("/unsign/{client_id}", response_model=StatusMessage)
async def unsign_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.unsign_client(client_id)
    return {"status": "application unsigned"}
unsign_client._meta = {"input_model": ClientIdIn}


# 10. Assign application to worker
@router.patch("/sign", response_model=StatusMessage)
async def sign_client(data: WorkerSignClientIn, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.sign_client(data.client_id, data.worker_id)
    return {"status": "application signed"}
sign_client._meta = {"input_model": WorkerSignClientIn}

from fastapi import Query

# 11. Get credits for month
@router.get("/credits/sum/monthly/{worker_id}")
async def get_credits_for_month(
    worker_id: UUID,
    month: str = Query(..., example="2025-06"),
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    total = await service.get_credits_for_month(worker_id, month)
    return {"value": total}

# 13. Get credits for year
@router.get("/credits/sum/yearly/{worker_id}")
async def get_credits_for_year(
    worker_id: UUID,
    year: int = Query(..., example=2025),
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    data = await service.get_credits_for_year(worker_id, year)
    return {"items": data}

# 14. Active credits count
@router.get("/active/count/{worker_id}")
async def get_active_credits_count(
    worker_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    count = await service.get_count_active_clients(worker_id)
    return {"count": count}

# 15. Completed credits count
@router.get("/completed/count/{worker_id}")
async def get_completed_credits_count(
    worker_id: UUID,
    db: AsyncSession = Depends(get_async_db)
):
    service = WorkerDashboardService(db)
    count = await service.get_count_completed_clients(worker_id)
    return {"count": count}

# 16. Get application by filters
@router.get(
    "/filter/bucket/{worker_id}",
    response_model=WorkerClientListOut,
    summary="Пагинированный список клиентов c фильтрами"
)
async def filter_bucket_clients_of_worker(
    worker_id: UUID,
    skip: int  = Query(0,  ge=0,  description="Сколько записей пропустить"),
    limit: int = Query(6,  ge=1,  le=100, description="Сколько вернуть"),
    email: str | None        = Query(None, description="Часть e-mail"),
    phone_number: str | None = Query(None, description="Часть номера"),
    full_name: str | None    = Query(None, description="Часть ФИО"),
    db: AsyncSession = Depends(get_async_db),
):
    service = WorkerDashboardService(db)

    clients, total = await service.filter_bucket_clients(
        worker_id=worker_id,
        skip=skip,
        limit=limit,
        email=email,
        phone_number=phone_number,
        full_name=full_name,
    )

    return {"clients": clients, "total": total}
