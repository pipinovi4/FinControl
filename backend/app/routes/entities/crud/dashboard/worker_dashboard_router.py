from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from db.session import get_async_db

from app.services.entities.worker.worker_dashboard import WorkerDashboardService
from app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    SimpleFloatOut,
    WorkerApplicationListOut,
    ApplicationIdIn,
    WorkerIdIn,
    WorkerBucketApplicationsIn,
    WorkerAssignApplicationIn,
    StatusMessage,
)

from app.schemas.entities.application_schema import (
    WorkerApplicationNewToday,
    ApplicationWorkerOut,
)

router = APIRouter(
    prefix="/application",
    tags=["worker:dashboard"]
)

# -----------------------------------------------------------
# 1. TOTAL APPLICATIONS
# -----------------------------------------------------------
@router.get("/sum/{worker_id}", response_model=SimpleIntOut)
async def get_applications_sum(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_applications(worker_id)}

get_applications_sum._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 2. TOTAL CREDITS
# -----------------------------------------------------------
@router.get("/credits/total/{worker_id}", response_model=SimpleFloatOut)
async def get_total_credits(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_total_sum_credits(worker_id)}

get_total_credits._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 3. MONTH CREDITS
# -----------------------------------------------------------
@router.get("/credits/month/{worker_id}", response_model=SimpleFloatOut)
async def get_month_credits(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_month_sum_credits(worker_id)}

get_month_credits._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 4. SUM DEALS
# -----------------------------------------------------------
@router.get("/deals-sum/{worker_id}", response_model=SimpleIntOut)
async def get_sum_deals(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_deals(worker_id)}

get_sum_deals._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 5. COUNT TODAY
# -----------------------------------------------------------
@router.get("/new-today/count/{worker_id}", response_model=SimpleIntOut)
async def get_sum_today_new(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_today_new_applications(worker_id)}

get_sum_today_new._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 6. COUNT YESTERDAY
# -----------------------------------------------------------
@router.get("/yesterday/count/{worker_id}", response_model=SimpleIntOut)
async def get_sum_yesterday_new(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_sum_yesterday_new_applications(worker_id)}

get_sum_yesterday_new._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 7. TODAY APPLICATIONS
# -----------------------------------------------------------
@router.get("/new-today/{worker_id}", response_model=list[WorkerApplicationNewToday])
async def get_today_new(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return await service.get_today_new_applications(worker_id)

get_today_new._meta = {"input_model": WorkerIdIn}


# -----------------------------------------------------------
# 8. PAGINATED APPLICATIONS
# -----------------------------------------------------------
@router.get("/bucket/{worker_id}", response_model=WorkerApplicationListOut)
async def get_bucket_applications(
    worker_id: UUID,
    skip: int = 0,
    limit: int = 8,
    db: AsyncSession = Depends(get_async_db),
):
    service = WorkerDashboardService(db)

    applications = await service.get_bucket_applications(worker_id, skip=skip, limit=limit)
    total = await service.get_sum_applications(worker_id)

    return {
        "applications": applications,
        "total": total
    }

get_bucket_applications._meta = {"input_model": WorkerBucketApplicationsIn}


# -----------------------------------------------------------
# 9. GET APPLICATION BY ID
# -----------------------------------------------------------
@router.get("/{application_id}", response_model=ApplicationWorkerOut)
async def get_application(application_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return await service.get_application(application_id)

get_application._meta = {"input_model": ApplicationIdIn}


# -----------------------------------------------------------
# 10. UNSIGN APPLICATION
# -----------------------------------------------------------
@router.patch("/unsign/{application_id}", response_model=StatusMessage)
async def unsign_application(application_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.unsign_application(application_id)
    return {"status": "application unsigned"}

unsign_application._meta = {"input_model": ApplicationIdIn}


# -----------------------------------------------------------
# 11. SIGN APPLICATION
# -----------------------------------------------------------
@router.patch("/sign", response_model=StatusMessage)
async def sign_application(data: WorkerAssignApplicationIn, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    await service.sign_application(data.application_id, data.worker_id)
    return {"status": "application signed"}

sign_application._meta = {"input_model": WorkerAssignApplicationIn}


# -----------------------------------------------------------
# 12. CREDITS FOR MONTH
# -----------------------------------------------------------
@router.get("/credits/sum/monthly/{worker_id}")
async def get_credits_for_month(
    worker_id: UUID,
    month: str = Query(..., example="2025-06"),
    db: AsyncSession = Depends(get_async_db),
):
    service = WorkerDashboardService(db)
    return {"items": await service.get_credits_for_month(worker_id, month)}


# -----------------------------------------------------------
# 13. CREDITS FOR YEAR
# -----------------------------------------------------------
@router.get("/credits/sum/yearly/{worker_id}")
async def get_credits_for_year(
    worker_id: UUID,
    year: int = Query(..., example=2025),
    db: AsyncSession = Depends(get_async_db),
):
    service = WorkerDashboardService(db)
    return {"items": await service.get_credits_for_year(worker_id, year)}


# -----------------------------------------------------------
# 14. ACTIVE APPLICATIONS COUNT
# -----------------------------------------------------------
@router.get("/active/count/{worker_id}", response_model=SimpleIntOut)
async def get_active_applications_count(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_count_active_applications(worker_id)}


# -----------------------------------------------------------
# 15. COMPLETED APPLICATIONS COUNT
# -----------------------------------------------------------
@router.get("/completed/count/{worker_id}", response_model=SimpleIntOut)
async def get_completed_applications_count(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = WorkerDashboardService(db)
    return {"value": await service.get_count_completed_applications(worker_id)}


# -----------------------------------------------------------
# 16. FILTERED BUCKET
# -----------------------------------------------------------
@router.get(
    "/filter/bucket/{worker_id}",
    response_model=WorkerApplicationListOut,
    summary="Пагинированный список заявок с фильтрами"
)
async def filter_bucket_applications(
    worker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1, le=100),
    email: str | None = Query(None),
    phone_number: str | None = Query(None),
    full_name: str | None = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    service = WorkerDashboardService(db)

    apps, total = await service.filter_bucket_applications(
        worker_id=worker_id,
        skip=skip,
        limit=limit,
        email=email,
        phone_number=phone_number,
        full_name=full_name,
    )

    return {
        "applications": apps,
        "total": total
    }
