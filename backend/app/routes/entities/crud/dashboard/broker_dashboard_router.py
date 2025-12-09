from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_db
from app.services.entities.broker.broker_dashboard import BrokerDashboard
from app.services.entities.credit.credit_service import CreditService, CreditStatus

from app.schemas.entities.application_schema import (
    ApplicationAdminOut,
    BrokerApplicationNewToday,
)
from app.schemas.entities.credit_schema import (
    CreditOut,
    CreditStatusUpdate,
    CreditCommentIn,
    BrokerPaginatedCreditsOut,
)
from app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    SimpleFloatOut,
    StatusMessage,
)

router = APIRouter(
    prefix="/application",
    tags=["broker:dashboard"]
)

# ────────────────────────────────────────────────
# 📌 1. TOTAL / MONTH / ACTIVE / COMPLETED CREDITS
# ────────────────────────────────────────────────

@router.get("/credits/count/total/{broker_id}", response_model=SimpleIntOut)
async def credits_total(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await BrokerDashboard(db).get_total_credits_count(broker_id)
    return SimpleIntOut(value=count)


@router.get("/credits/count/month/{broker_id}", response_model=SimpleIntOut)
async def credits_month(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await BrokerDashboard(db).get_month_credits_count(broker_id)
    return SimpleIntOut(value=count)


@router.get("/credits/count/active/{broker_id}", response_model=SimpleIntOut)
async def credits_active(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await BrokerDashboard(db).get_count_active_credits(broker_id)
    return SimpleIntOut(value=count)


@router.get("/credits/count/completed/{broker_id}", response_model=SimpleIntOut)
async def credits_completed(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await BrokerDashboard(db).get_count_completed_credits(broker_id)
    return SimpleIntOut(value=count)


# ────────────────────────────────────────────────
# 📌 2. APPLICATIONS STATS
# ────────────────────────────────────────────────

@router.get("/assigned/sum/{broker_id}", response_model=SimpleIntOut)
async def applications_assigned_sum(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await BrokerDashboard(db).get_sum_signed_applications(broker_id)
    return SimpleIntOut(value=total)


# ────────────────────────────────────────────────
# 📌 3. PAGINATED APPLICATION BUCKETS
# ────────────────────────────────────────────────

@router.get("/assigned/bucket/{broker_id}", response_model=dict)
async def assigned_bucket(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    service = BrokerDashboard(db)
    applications = await service.get_bucket_signed_applications(broker_id, skip=skip, limit=limit)
    total = await service.get_sum_signed_applications(broker_id)

    return {
        "applications": [ApplicationAdminOut.model_validate(a) for a in applications],
        "total": total,
    }


@router.get("/unassigned/bucket/{broker_id}", response_model=dict)
async def unassigned_bucket(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(8, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    service = BrokerDashboard(db)
    applications = await service.get_bucket_unsigned_applications(broker_id, skip=skip, limit=limit)

    return {
        "applications": [ApplicationAdminOut.model_validate(a) for a in applications],
        "total": len(applications),
    }


# ────────────────────────────────────────────────
# 📌 4. SINGLE APPLICATION
# ────────────────────────────────────────────────

@router.get("/{app_id}", response_model=ApplicationAdminOut)
async def get_application(app_id: UUID, db: AsyncSession = Depends(get_async_db)):
    app = await BrokerDashboard(db).get_application(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


# ────────────────────────────────────────────────
# 📌 5. ASSIGN / UNASSIGN APPLICATION
# ────────────────────────────────────────────────

@router.patch("/assign/{app_id}/{broker_id}", response_model=StatusMessage)
async def assign(app_id: UUID, broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await BrokerDashboard(db).assign_application(app_id, broker_id)
    return {"status": "assigned"}


@router.patch("/unassign/{app_id}", response_model=StatusMessage)
async def unassign(app_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await BrokerDashboard(db).unassign_application(app_id)
    return {"status": "unassigned"}


# ────────────────────────────────────────────────
# 📌 6. CREATE CREDIT FROM APPLICATION
# ────────────────────────────────────────────────

@router.post("/credit/{app_id}/{broker_id}", response_model=CreditOut)
async def create_credit(
    app_id: UUID,
    broker_id: UUID,
    amount: float = Query(..., gt=0),
    db: AsyncSession = Depends(get_async_db),
):
    credit = await BrokerDashboard(db).create_credit(app_id, broker_id, amount)
    return CreditOut.model_validate(credit)


# ────────────────────────────────────────────────
# 📌 7. TODAY / YESTERDAY METRICS
# ────────────────────────────────────────────────

@router.get("/new-today/count/{broker_id}", response_model=SimpleIntOut)
async def count_today(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await BrokerDashboard(db).get_sum_today_new_applications(broker_id)
    return SimpleIntOut(value=total)


@router.get("/new-yesterday/count/{broker_id}", response_model=SimpleIntOut)
async def count_yesterday(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await BrokerDashboard(db).get_sum_yesterday_new_applications(broker_id)
    return SimpleIntOut(value=total)


@router.get("/new-today/{broker_id}", response_model=list[BrokerApplicationNewToday])
async def today_list(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await BrokerDashboard(db).get_today_new_applications(broker_id)


# ────────────────────────────────────────────────
# 📌 8. COMMISSIONS SUMS
# ────────────────────────────────────────────────

@router.get("/credits/sum/total/{broker_id}", response_model=SimpleFloatOut)
async def sum_total(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await BrokerDashboard(db).get_sum_broker_commissions(broker_id)
    return SimpleFloatOut(value=total)


@router.get("/credits/sum/month/{broker_id}", response_model=SimpleFloatOut)
async def sum_month(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await BrokerDashboard(db).get_month_broker_commissions(broker_id)
    return SimpleFloatOut(value=total)


# ────────────────────────────────────────────────
# 📌 9. CREDITS LIST FOR BROKER (PAGINATED)
# ────────────────────────────────────────────────

@router.get("/credits/{broker_id}", response_model=BrokerPaginatedCreditsOut)
async def credits_list(
    broker_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=200),
    statuses: Optional[List[CreditStatus]] = Query(None),
    application_id: Optional[UUID] = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    items, total = await CreditService(db).list_for_broker_paginated(
        broker_id,
        skip=skip,
        limit=limit,
        statuses=statuses,
        application_id=application_id,
        created_from=created_from,
        created_to=created_to,
    )
    return BrokerPaginatedCreditsOut(
        credits=[CreditOut.model_validate(i) for i in items],
        total=total
    )


# ────────────────────────────────────────────────
# 📌 10. CREDIT → GET / UPDATE STATUS / COMMENT
# ────────────────────────────────────────────────

@router.get("/credit/{broker_id}/{credit_id}", response_model=CreditOut)
async def credit_get(broker_id: UUID, credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    credit = await CreditService(db).get_for_broker(credit_id, broker_id)
    return CreditOut.model_validate(credit)


@router.patch("/credit/{broker_id}/{credit_id}/status", response_model=CreditOut)
async def credit_status(
    broker_id: UUID,
    credit_id: UUID,
    payload: CreditStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    service = CreditService(db)
    await service.get_for_broker(credit_id, broker_id)
    updated = await service.broker_update_status(credit_id, payload.status)
    return CreditOut.model_validate(updated)


@router.post("/credit/{broker_id}/{credit_id}/comment", response_model=CreditOut)
async def credit_comment(
    broker_id: UUID,
    credit_id: UUID,
    payload: CreditCommentIn,
    db: AsyncSession = Depends(get_async_db),
):
    service = CreditService(db)
    await service.get_for_broker(credit_id, broker_id)
    updated = await service.add_comment(credit_id, payload.text)
    return CreditOut.model_validate(updated)
