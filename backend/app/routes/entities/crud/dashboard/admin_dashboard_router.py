from __future__ import annotations
from datetime import date, datetime
from typing import Any, Dict, Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Body, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_db
from app.routes.entities.crud.dashboard.types import (
    DeletedFilter,
    SimpleIntOut,
    StatusMessage,
)
from app.schemas.auth.invite_schema import InviteIn, InviteOut

from app.schemas.entities.application_schema import (
    ApplicationAdminOut,
    WorkerApplicationNewToday,
    BrokerApplicationNewToday,
    ApplicationNewToday,
)
from app.schemas.entities.worker_schema import WorkerAdminOut
from app.schemas.entities.broker_schema import BrokerAdminOut

from app.schemas.entities.credit_schema import (
    CreditOut,
    CreditCreate,
    CreditUpdate,
    CreditCommentIn,
    AdminPaginatedCreditsOut,
)
from app.schemas.entities.promotion_schema import (
    PromotionCreate,
    PromotionUpdate,
    PromotionOut,
    PromotionSummaryOut,
    TopWorkerOut,
)
from app.models.entities.promotion import PromotionEnum
from app.services.entities.promotion.promotion_service import PromotionService
from app.services.auth.invite_service import InviteService
from app.services.entities.credit.credit_service import CreditService, CreditStatus

from app.services.entities.admin.admin_dashboard import AdminDashboard


router = APIRouter(tags=["admin:dashboard"])


# ───────────────────────────────────────────────
# INVITES
# ───────────────────────────────────────────────
@router.post("/create-invite", response_model=InviteOut)
async def create_invite(data: InviteIn, db: AsyncSession = Depends(get_async_db)):
    raw = await InviteService(db).create_invite(role=data.role, expires_at=data.expires_at)
    return {"raw": raw}


# ───────────────────────────────────────────────
# GLOBAL SUMMARY
# ───────────────────────────────────────────────
@router.get("/applications/total", response_model=SimpleIntOut)
async def total_applications(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_applications()
    return {"value": total}


@router.get("/credits/total", response_model=SimpleIntOut)
async def total_credits(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_total_sum_credits()
    return {"value": total}


@router.get("/credits/month", response_model=SimpleIntOut)
async def month_credits(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_month_sum_credits()
    return {"value": total}


@router.get("/users/total", response_model=SimpleIntOut)
async def total_users(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_users()
    return {"value": total}


@router.get("/workers/total", response_model=SimpleIntOut)
async def total_workers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_workers()
    return {"value": total}


@router.get("/brokers/total", response_model=SimpleIntOut)
async def total_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_brokers()
    return {"value": total}


@router.get("/credits/count", response_model=SimpleIntOut)
async def credits_count(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_credits()
    return {"value": total}


# ───────────────────────────────────────────────
# DATE RANGE
# ───────────────────────────────────────────────
@router.get("/credits/range", response_model=SimpleIntOut)
async def credits_range(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    amount = await AdminDashboard(db).get_sum_credits_by_date(date_from, date_to)
    return {"value": amount}


# ───────────────────────────────────────────────
# NEW TODAY — APPLICATIONS
# ───────────────────────────────────────────────
@router.get("/workers/applications/new-today/{admin_id}", response_model=list[WorkerApplicationNewToday])
async def today_new_apps_worker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_applications_worker()


@router.get("/workers/applications/new-yesterday/{admin_id}", response_model=list[WorkerApplicationNewToday])
async def yesterday_new_apps_worker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_applications_worker()


@router.get("/brokers/applications/new-today/{admin_id}", response_model=list[BrokerApplicationNewToday])
async def today_new_apps_broker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_applications_broker()


@router.get("/brokers/applications/new-yesterday/{admin_id}", response_model=list[BrokerApplicationNewToday])
async def yesterday_new_apps_broker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_applications_broker()


# ───────────────────────────────────────────────
# NEW WORKERS / BROKERS
# ───────────────────────────────────────────────
@router.get("/workers/new-today/{admin_id}", response_model=list[ApplicationNewToday])
async def today_new_workers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_workers()


@router.get("/workers/new-yesterday/{admin_id}", response_model=list[ApplicationNewToday])
async def yesterday_new_workers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_workers()


@router.get("/brokers/new-today/{admin_id}", response_model=list[ApplicationNewToday])
async def today_new_brokers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_brokers()


@router.get("/brokers/new-yesterday/{admin_id}", response_model=list[ApplicationNewToday])
async def yesterday_new_brokers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_brokers()


# ───────────────────────────────────────────────
# BUCKET: APPLICATIONS
# ───────────────────────────────────────────────

class AdminPaginatedApplicationsOut(BaseModel):
    applications: list[ApplicationAdminOut]
    total: int


@router.get("/applications/{admin_id}", response_model=AdminPaginatedApplicationsOut)
async def bucket_applications(
    admin_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    search: Optional[str] = Query(None),
    deleted: DeletedFilter = Query("all"),
    db: AsyncSession = Depends(get_async_db),
):
    apps, total = await AdminDashboard(db).get_bucket_applications(
        skip=skip, limit=limit, search=search, deleted=deleted
    )
    return {"applications": apps, "total": total}


# ───────────────────────────────────────────────
# SINGLE ENTITIES
# ───────────────────────────────────────────────
@router.get("/application/{app_id}", response_model=ApplicationAdminOut)
async def get_application(app_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_application(app_id)


@router.get("/worker/{worker_id}", response_model=WorkerAdminOut)
async def get_worker(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_worker(worker_id)


@router.get("/broker/{broker_id}", response_model=BrokerAdminOut)
async def get_broker(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_broker(broker_id)


# ───────────────────────────────────────────────
# DELETE / RESTORE USER
# ───────────────────────────────────────────────
@router.patch("/user/{user_id}/deactivate", response_model=StatusMessage)
async def deactivate_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).delete_user(user_id)
    return {"status": "deactivated"}


@router.patch("/user/{user_id}/restore", response_model=StatusMessage)
async def restore_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).restore_user(user_id, reactivate=True)
    return {"status": "restored"}


# ───────────────────────────────────────────────
# REASSIGN APPLICATIONS
# ───────────────────────────────────────────────
@router.patch("/application/{app_id}/assign-worker-by-email", response_model=StatusMessage)
async def assign_worker_by_email(
    app_id: UUID,
    worker_email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).worker_reassign_applications_by_email(app_id, worker_email)
    return {"status": "reassigned", "worker_email": worker_email}


@router.patch("/application/{app_id}/assign-broker-by-email", response_model=StatusMessage)
async def assign_broker_by_email(
    app_id: UUID,
    broker_email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).broker_reassign_application_by_email(app_id, broker_email)
    return {"status": "reassigned", "broker_email": broker_email}


# ───────────────────────────────────────────────
# CREDIT CONTROL
# ───────────────────────────────────────────────
@router.patch("/credit/{credit_id}/force-complete", response_model=StatusMessage)
async def force_complete_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).force_complete_credit(credit_id)
    return {"status": "completed"}


@router.patch("/credit/{credit_id}/status", response_model=StatusMessage)
async def change_credit_status(
    credit_id: UUID,
    new_status: str = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).change_credit_status(credit_id, new_status)
    return {"status": "updated", "new_status": new_status}


# ───────────────────────────────────────────────
# EDIT ENTITIES
# ───────────────────────────────────────────────
@router.patch("/application/{app_id}", response_model=StatusMessage)
async def edit_application(app_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).edit_application_data(app_id, fields)
    return {"status": "updated"}


@router.patch("/broker/{broker_id}", response_model=StatusMessage)
async def edit_broker(broker_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).edit_broker_data(broker_id, fields)
    return {"status": "updated"}


@router.patch("/worker/{worker_id}", response_model=StatusMessage)
async def edit_worker(worker_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).edit_worker_data(worker_id, fields)
    return {"status": "updated"}


# ───────────────────────────────────────────────
# CREDIT LIST / UPDATE / DELETE
# ───────────────────────────────────────────────

@router.post("/credits", response_model=CreditOut)
async def admin_create_credit(payload: CreditCreate, db: AsyncSession = Depends(get_async_db)):
    credit = await CreditService(db).create(payload)
    return CreditOut.model_validate(credit)


@router.get("/credits/{credit_id}", response_model=CreditOut)
async def admin_get_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    credit = await CreditService(db).get_by_id(credit_id)
    if not credit:
        raise HTTPException(404, "Credit not found")
    return CreditOut.model_validate(credit)


@router.get("/credits", response_model=AdminPaginatedCreditsOut)
async def admin_list_credits(
    skip: int = Query(0),
    limit: int = Query(20),
    statuses: List[CreditStatus] | None = Query(None),
    broker_id: UUID | None = Query(None),
    application_id: UUID | None = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    deleted: DeletedFilter = Query("active"),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    items, total = await CreditService(db).list_paginated(
        skip=skip, limit=limit,
        statuses=statuses,
        broker_id=broker_id,
        application_id=application_id,
        created_from=created_from,
        created_to=created_to,
        deleted=deleted,
        search=search,
    )
    return AdminPaginatedCreditsOut(
        credits=[CreditOut.model_validate(c) for c in items],
        total=total,
    )


@router.patch("/credits/{credit_id}", response_model=CreditOut)
async def admin_update_credit(
    credit_id: UUID,
    payload: CreditUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    updated = await CreditService(db).update(credit_id, payload)
    return CreditOut.model_validate(updated)


@router.post("/credits/{credit_id}/comment", response_model=CreditOut)
async def admin_add_comment(
    credit_id: UUID,
    comment: CreditCommentIn,
    db: AsyncSession = Depends(get_async_db),
):
    updated = await CreditService(db).add_comment(credit_id, comment.text)
    return CreditOut.model_validate(updated)


@router.delete("/credits/{credit_id}", status_code=204)
async def admin_soft_delete_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await CreditService.soft_delete(db, credit_id)
    return Response(status_code=204)


@router.patch("/credits/{credit_id}/restore", response_model=CreditOut)
async def admin_restore_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await CreditService.restore(db, credit_id)
    credit = await CreditService(db).get_by_id(credit_id)
    return CreditOut.model_validate(credit)
