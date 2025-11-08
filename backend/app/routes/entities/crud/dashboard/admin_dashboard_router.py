from __future__ import annotations

# backend/app/routers/dashboard/admin_credits.py
from datetime import date, datetime
from typing import Any, Dict, Optional, List, Literal
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Body, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.entities.crud.dashboard.types import DeletedFilter
from app.schemas import WorkerSchema, BrokerSchema, ClientSchema
from app.schemas.auth.invite_schema import InviteIn, InviteOut
from app.schemas.entities.client_schema import WorkerClientNewToday, UserNewToday
from app.services.auth.invite_service import InviteService
from backend.db.session import get_async_db
from app.services.entities.admin.admin_dashboard import AdminDashboard
from app.models.entities.promotion import PromotionEnum
from app.services.entities.promotion.promotion_service import PromotionService
from app.services.entities.credit.credit_service import CreditService, CreditStatus
from app.schemas.entities.credit_schema import (
    CreditOut, CreditCreate, CreditUpdate, CreditCommentIn, AdminPaginatedCreditsOut
)
from app.schemas.entities.promotion_schema import (
    PromotionCreate, PromotionUpdate, PromotionOut, PromotionSummaryOut, TopWorkerOut
)
from app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    StatusMessage,
    AdminPaginatedClientsOut,
    AdminPaginatedWorkersOut,
    AdminPaginatedBrokersOut,
    BucketIn,
    WorkerIdIn,
    ClientIdIn,
    BrokerIdIn, BrokerClientListOut,
)

router = APIRouter(tags=["admin:dashboard"])

# --- INVITES ---
@router.post("/create-invite", response_model=InviteOut)
async def create_invite(data: InviteIn, db: AsyncSession = Depends(get_async_db)):
    raw = await InviteService(db).create_invite(role=data.role, expires_at=data.expires_at)
    return {"raw": raw}

# --- GLOBAL ---
@router.get("/credits/total", response_model=SimpleIntOut)
async def total_credits(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_total_sum_credits()
    return {"value": amount}

@router.get("/credits/month", response_model=SimpleIntOut)
async def month_credits(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_month_sum_credits()
    return {"value": amount}

@router.get("/users/total", response_model=SimpleIntOut)
async def total_users(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_users()
    return {"value": total}

@router.get("/clients/total", response_model=SimpleIntOut)
async def total_clients(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_clients()
    return {"value": total}

@router.get("/brokers/total", response_model=SimpleIntOut)
async def total_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_brokers()
    return {"value": total}

@router.get("/workers/total", response_model=SimpleIntOut)
async def total_workers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_workers()
    return {"value": total}

@router.get("/credits/count", response_model=SimpleIntOut)
async def credits_count(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_credits()
    return {"value": total}

# --- RANGE ---
@router.get("/credits/range", response_model=SimpleIntOut)
async def credits_range(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    amount = await AdminDashboard(db).get_sum_credits_by_date(date_from, date_to)
    return {"value": amount}

# --- PER-WORKER / PER-BROKER NEW ---
@router.get("/workers/clients/new-today/{admin_id}", response_model=list[WorkerClientNewToday])
async def today_new_clients_worker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_clients_worker()
today_new_clients_worker._meta = {"input_model": WorkerIdIn}

@router.get("/workers/clients/new-yesterday/{admin_id}", response_model=list[WorkerClientNewToday])
async def yesterday_new_clients_worker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_clients_worker()
yesterday_new_clients_worker._meta = {"input_model": WorkerIdIn}

@router.get("/brokers/clients/new-today/{admin_id}", response_model=list[WorkerClientNewToday])
async def today_new_clients_broker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_clients_broker()
today_new_clients_broker._meta = {"input_model": WorkerIdIn}

@router.get("/brokers/clients/new-yesterday/{admin_id}", response_model=list[WorkerClientNewToday])
async def yesterday_new_clients_broker(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_clients_broker()
yesterday_new_clients_broker._meta = {"input_model": WorkerIdIn}

@router.get("/workers/new-today/{admin_id}", response_model=list[UserNewToday])
async def today_new_workers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_workers()
today_new_workers._meta = {"input_model": WorkerIdIn}

@router.get("/workers/new-yesterday/{admin_id}", response_model=list[UserNewToday])
async def yesterday_new_workers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_workers()
yesterday_new_workers._meta = {"input_model": WorkerIdIn}

@router.get("/brokers/new-today/{admin_id}", response_model=list[UserNewToday])
async def today_new_brokers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_today_new_brokers()
today_new_brokers._meta = {"input_model": WorkerIdIn}

@router.get("/brokers/new-yesterday/{admin_id}", response_model=list[UserNewToday])
async def yesterday_new_brokers(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_yesterday_new_brokers()
yesterday_new_brokers._meta = {"input_model": WorkerIdIn}

@router.get("/workers/{worker_id}/clients/signed-count", response_model=SimpleIntOut)
async def signed_by_worker(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_signed_clients_by_worker(worker_id)
    return {"value": total}
signed_by_worker._meta = {"input_model": WorkerIdIn}

@router.get("/workers/{worker_id}/clients/unsigned-count", response_model=SimpleIntOut)
async def unsigned_by_worker(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_unsigned_clients_by_worker()
    return {"value": total}
unsigned_by_worker._meta = {"input_model": WorkerIdIn}

# --- BROKER TOTALS ---
@router.get("/brokers/clients/signed-count", response_model=SimpleIntOut)
async def signed_by_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_total_count_signed_clients_by_brokers()
    return {"value": total}

@router.get("/brokers/clients/unsigned-count", response_model=SimpleIntOut)
async def unsigned_by_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_total_count_unsigned_clients_by_brokers()
    return {"value": total}

# --- BUCKETS ---
@router.get("/clients/{admin_id}", response_model=AdminPaginatedClientsOut)
async def bucket_clients(
    admin_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    search: Optional[str] = Query(None, description="Поиск по ФИО/email/телефону/адресу/UUID"),
    deleted: DeletedFilter = Query("all", description="'active' | 'only' | 'all'"),
    db: AsyncSession = Depends(get_async_db),
):
    items, total = await AdminDashboard(db).get_bucket_clients(skip=skip, limit=limit, search=search, deleted=deleted)
    return {"clients": items, "total": total}

@router.get("/brokers/{admin_id}", response_model=AdminPaginatedBrokersOut)
async def bucket_brokers(
    admin_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    deleted: DeletedFilter = Query("all", description="'active' | 'only' | 'all'"),
    db: AsyncSession = Depends(get_async_db),
):
    items, total = await AdminDashboard(db).get_bucket_brokers(skip=skip, limit=limit, deleted=deleted)
    return {"clients": items, "total": total}

@router.get("/workers/{admin_id}", response_model=AdminPaginatedWorkersOut)
async def bucket_workers(
    admin_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    deleted: DeletedFilter = Query("all", description="'active' | 'only' | 'all'"),
    db: AsyncSession = Depends(get_async_db),
):
    items, total = await AdminDashboard(db).get_bucket_workers(skip=skip, limit=limit, deleted=deleted)
    return {"clients": items, "total": total}

# --- SINGLE ENTITIES ---
@router.get("/client/{client_id}")
async def get_client(client_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_client(client_id)
get_client._meta = {"input_model": ClientIdIn}

@router.get("/worker/{worker_id}")
async def get_worker(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_worker(worker_id)
get_worker._meta = {"input_model": WorkerIdIn}

@router.get("/broker/{broker_id}")
async def get_broker(broker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_broker(broker_id)
get_broker._meta = {"input_model": BrokerIdIn}

# --- SOFT DELETE / RESTORE ---
@router.patch("/user/{user_id}/deactivate", response_model=StatusMessage)
async def deactivate_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).delete_user(user_id)
    return {"status": "deactivated"}

@router.patch("/user/{user_id}/restore", response_model=StatusMessage)
async def restore_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).restore_user(user_id, reactivate=True)
    return {"status": "restored"}

# --- REASSIGNMENT ---
@router.patch("/client/{client_id}/assign-worker-by-email", response_model=StatusMessage)
async def assign_worker_by_email(
    client_id: UUID,
    worker_email: Optional[str] = Query(None, description="Email воркера; None → отвязать"),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).worker_reassign_client_by_email(client_id, worker_email)
    return {"status": "reassigned", "worker_email": worker_email}

@router.patch("/client/{client_id}/assign-broker-by-email", response_model=StatusMessage)
async def assign_broker_by_email(
    client_id: UUID,
    broker_email: Optional[str] = Query(None, description="Email брокера; None → отвязать"),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).broker_reassign_client_by_email(client_id, broker_email)
    return {"status": "reassigned", "broker_email": broker_email}

# --- CREDIT CONTROL ---
@router.patch("/credit/{credit_id}/force-complete", response_model=StatusMessage)
async def force_complete_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).force_complete_credit(credit_id)
    return {"status": "completed"}

@router.patch("/credit/{credit_id}/status", response_model=StatusMessage)
async def change_credit_status(credit_id: UUID, new_status: str = Query(...), db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).change_credit_status(credit_id, new_status)
    return {"status": "updated", "new_status": new_status}

# --- EDIT ENTITIES ---
@router.patch("/client/{client_id}", response_model=StatusMessage)
async def edit_client(client_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    payload = ClientSchema.Update(**fields)
    await AdminDashboard(db).edit_client_data(client_id, payload.model_dump(exclude_unset=True))
    return {"status": "updated"}

@router.patch("/broker/{broker_id}", response_model=StatusMessage)
async def edit_broker(broker_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    payload = BrokerSchema.Update(**fields)
    await AdminDashboard(db).edit_broker_data(broker_id, payload.model_dump(exclude_unset=True))
    return {"status": "updated"}

@router.patch("/worker/{worker_id}", response_model=StatusMessage)
async def edit_worker(worker_id: UUID, fields: Dict[str, Any] = Body(...), db: AsyncSession = Depends(get_async_db)):
    payload = WorkerSchema.Update(**fields)
    await AdminDashboard(db).edit_worker_data(worker_id, payload.model_dump(exclude_unset=True))
    return {"status": "updated"}

# --- CREDITS STATS ---
@router.get("/credits/sum/monthly")
async def credits_sum_monthly(
    month: str = Query(..., example="2025-06"),
    db: AsyncSession = Depends(get_async_db),
):
    service = AdminDashboard(db)
    items = await service.get_credits_for_month(month)
    return items

@router.get("/credits/sum/yearly")
async def credits_sum_yearly(
    year: int = Query(..., example=2025),
    db: AsyncSession = Depends(get_async_db),
):
    service = AdminDashboard(db)
    items = await service.get_credits_for_year(year)
    return items

# --- CREDITS COUNTS ---
@router.get("/credits/count/active/{admin_id}", response_model=SimpleIntOut)
async def get_active_credits_count(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await AdminDashboard(db).get_count_active_credits()
    return SimpleIntOut(value=count)
get_active_credits_count._meta = {"input_model": BrokerIdIn}

@router.get("/credits/count/completed/{admin_id}", response_model=SimpleIntOut)
async def get_completed_credits_count(admin_id: UUID, db: AsyncSession = Depends(get_async_db)):
    count = await AdminDashboard(db).get_count_completed_credits()
    return SimpleIntOut(value=count)
get_completed_credits_count._meta = {"input_model": BrokerIdIn}

# --- FILTER BUCKETS with is_deleted ---
@router.get("/clients/filter/bucket/{admin_id}", response_model=BrokerClientListOut, summary="Пагинированный список клиентов c фильтрами")
async def filter_bucket_clients_of_admins(
    admin_id: UUID,
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(6, ge=1, le=100, description="Сколько вернуть"),
    email: str | None = Query(None, description="Часть e-mail"),
    phone_number: str | None = Query(None, description="Часть номера"),
    full_name: str | None = Query(None, description="Часть ФИО"),
    is_deleted: bool | None = Query(None, description="true — удалённые, false — активные, None — все"),
    db: AsyncSession = Depends(get_async_db),
):
    service = AdminDashboard(db)
    clients, total = await service.filter_bucket_clients(
        skip=skip, limit=limit, email=email, phone_number=phone_number, full_name=full_name, is_deleted=is_deleted
    )
    return {"clients": clients, "total": total}

@router.get("/workers/filter/bucket/{admin_id}", response_model=AdminPaginatedWorkersOut, summary="Пагинированный список работников c фильтрами")
async def filter_bucket_workers_for_admins(
    admin_id: UUID,
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(6, ge=1, le=100, description="Сколько вернуть"),
    email: str | None = Query(None, description="Часть e-mail"),
    username: str | None = Query(None, description="Часть никнейма"),
    is_deleted: bool | None = Query(None, description="true — удалённые, false — активные, None — все"),
    db: AsyncSession = Depends(get_async_db),
):
    service = AdminDashboard(db)
    workers, total = await service.filter_bucket_workers(skip=skip, limit=limit, email=email, username=username, is_deleted=is_deleted)
    return {"clients": workers, "total": total}

@router.get("/brokers/filter/bucket/{admin_id}", response_model=AdminPaginatedBrokersOut, summary="Пагинированный список брокеров c фильтрами")
async def filter_bucket_brokers_for_admins(
    admin_id: UUID,
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(6, ge=1, le=100, description="Сколько вернуть"),
    email: str | None = Query(None, description="Часть e-mail"),
    company_name: str | None = Query(None, description="Часть компании"),
    region: str | None = Query(None, description="Часть региона"),
    is_deleted: bool | None = Query(None, description="true — удалённые, false — активные, None — все"),
    db: AsyncSession = Depends(get_async_db),
):
    service = AdminDashboard(db)
    brokers, total = await service.filter_bucket_brokers(
        skip=skip, limit=limit, email=email, company_name=company_name, region=region, is_deleted=is_deleted
    )
    return {"clients": brokers, "total": total}

# --- PROMOTIONS (unchanged) ---
@router.get("/promotions/top-workers", response_model=list[TopWorkerOut], tags=["admin:promotions"])
async def top_workers_by_credits_count(limit: int = Query(3, ge=1, le=20), db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).top_workers_by_count(limit=limit)

@router.get("/promotions/summary", response_model=list[PromotionSummaryOut], tags=["admin:promotions"])
async def list_promotions_summary(ptype: PromotionEnum | None = Query(None), limit: int = Query(12, ge=1, le=200), db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).list_promotions_summary(ptype=ptype, limit=limit)

@router.get("/promotions", response_model=list[PromotionOut], tags=["admin:promotions"])
async def list_promotions(
    is_active: bool | None = Query(None),
    ptype: PromotionEnum | None = Query(None),
    limit: int = Query(8, ge=1, le=200),
    db: AsyncSession = Depends(get_async_db),
):
    return await PromotionService.list(db, limit=limit, ptype=(ptype.value if ptype else None), is_active=is_active, include_deleted=False)

@router.post("/promotions", response_model=PromotionOut, tags=["admin:promotions"])
async def create_promotion(payload: PromotionCreate, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).create_promotion(payload)

@router.get("/promotions/{promo_id}", response_model=PromotionOut, tags=["admin:promotions"])
async def get_promotion(promo_id: UUID, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).get_promotion(promo_id)

@router.patch("/promotions/{promo_id}", response_model=PromotionOut, tags=["admin:promotions"])
async def update_promotion(promo_id: UUID, payload: PromotionUpdate, db: AsyncSession = Depends(get_async_db)):
    return await AdminDashboard(db).update_promotion(promo_id, payload)

@router.patch("/promotions/{promo_id}/activate", response_model=PromotionOut, tags=["admin:promotions"])
async def activate_promotion(
    promo_id: UUID,
    deactivate_others_same_type: bool = Query(False, description="Выключить другие активные промо этого же типа"),
    db: AsyncSession = Depends(get_async_db),
):
    return await AdminDashboard(db).activate_promotion(promo_id, deactivate_others_same_type=deactivate_others_same_type)

@router.patch("/promotions/{promo_id}/deactivate", tags=["admin:promotions"])
async def deactivate_promotion(promo_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).deactivate_promotion(promo_id)
    return {"status": "deactivated", "id": str(promo_id)}

@router.delete("/promotions/{promotion_id}", status_code=204, tags=["admin:promotions"])
async def soft_delete_promotion(promotion_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await PromotionService.soft_delete(db, promotion_id)
    return Response(status_code=204)

# ───────────────────────────────────────────────
# ADMIN: CREDITS
# ───────────────────────────────────────────────

@router.post("/credits", response_model=CreditOut, tags=["admin:credits"])
async def admin_create_credit(payload: CreditCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Створює кредит для клієнта (адмін). broker_id береться з Client.
    """
    service = CreditService(db)
    credit = await service.create(payload)
    return CreditOut.model_validate(credit)


@router.get("/credits/{credit_id}", response_model=CreditOut, tags=["admin:credits"])
async def admin_get_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    credit = await CreditService(db).get_by_id(credit_id)
    if not credit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit not found")
    return CreditOut.model_validate(credit)

@router.get("/credits", response_model=AdminPaginatedCreditsOut, tags=["admin:credits"])
async def admin_list_credits(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    statuses: List[CreditStatus] | None = Query(None),
    broker_id: UUID | None = Query(None),
    client_id: UUID | None = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    deleted: DeletedFilter = Query("active", description="'active'| 'only' | 'all'"),
    search: Optional[str] = Query(None, description="id кредита, email/телефон/ФИО клиента"),
    db: AsyncSession = Depends(get_async_db),
):
    service = CreditService(db)
    items, total = await service.list_paginated(
        skip=skip, limit=limit, statuses=statuses,
        broker_id=broker_id, client_id=client_id,
        created_from=created_from, created_to=created_to,
        deleted=deleted, search=search,
    )
    return AdminPaginatedCreditsOut(
        credits=[CreditOut.model_validate(c) for c in items],
        total=total,
    )


@router.patch("/credits/{credit_id}", response_model=CreditOut, tags=["admin:credits"])
async def admin_update_credit(
    credit_id: UUID,
    payload: CreditUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Адмін може змінювати будь-які поля кредиту (включно з фінпараметрами і статусом).
    """
    service = CreditService(db)
    updated = await service.update(credit_id, payload)
    return CreditOut.model_validate(updated)


@router.patch("/credits/{credit_id}/status", response_model=CreditOut, tags=["admin:credits"])
async def admin_change_credit_status(
    credit_id: UUID,
    new_status: CreditStatus = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    updated = await CreditService(db).change_status(credit_id, new_status)
    return CreditOut.model_validate(updated)


@router.post("/credits/{credit_id}/comment", response_model=CreditOut, tags=["admin:credits"])
async def admin_add_comment(
    credit_id: UUID,
    comment: CreditCommentIn,
    db: AsyncSession = Depends(get_async_db),
):
    updated = await CreditService(db).add_comment(credit_id, comment.text)
    return CreditOut.model_validate(updated)


@router.delete("/credits/{credit_id}", status_code=204, tags=["admin:credits"])
async def admin_soft_delete_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await CreditService.soft_delete(db, credit_id)
    return Response(status_code=204)

@router.patch("/credits/{credit_id}/restore", status_code=200, response_model=CreditOut, tags=["admin:credits"])
async def admin_restore_credit(credit_id: UUID, db: AsyncSession = Depends(get_async_db)):
    credit = await CreditService(db).get_by_id(credit_id)
    if not credit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credit not found")
    await CreditService.restore(db, credit_id)
    credit = await CreditService(db).get_by_id(credit_id)
    return CreditOut.model_validate(credit)
