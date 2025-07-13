# routers/admin_dashboard_router.py
from __future__ import annotations

from datetime import date
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_async_db
from backend.app.services.entities.admin.admin_dashboard import AdminDashboard
from backend.app.routes.entities.crud.dashboard.types import (
    SimpleIntOut,
    SimpleFloatOut,
    StatusMessage,
    PaginatedClientsOut,
    PaginatedWorkersOut,
    PaginatedBrokersOut,
    BucketIn,
    WorkerIdIn,
    ClientIdIn,
    BrokerIdIn,
)

router = APIRouter(
    tags=["admin:dashboard"],
)

# ──────────────── 📊 GLOBAL AGGREGATES ────────────────
@router.get("/earnings/total", response_model=SimpleFloatOut)
async def total_earnings(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_total_sum_earnings()
    return {"value": amount}

@router.get("/credits/total", response_model=SimpleIntOut)
async def total_credits(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_total_sum_credits()
    return {"value": amount}

@router.get("/earnings/month", response_model=SimpleFloatOut)
async def month_earnings(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_month_sum_earnings()
    return {"value": amount}

@router.get("/credits/month", response_model=SimpleIntOut)
async def month_credits(db: AsyncSession = Depends(get_async_db)):
    amount = await AdminDashboard(db).get_month_sum_credits()
    return {"value": amount}

@router.get("/clients/total", response_model=SimpleIntOut)
async def total_clients(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_clients()
    return {"value": total}

@router.get("/brokers/total", response_model=SimpleIntOut)
async def total_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_brokers()
    return {"value": total}

@router.get("/credits/count", response_model=SimpleIntOut)
async def credits_count(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_credits()
    return {"value": total}

@router.get("/deals/count", response_model=SimpleIntOut)
async def deals_count(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_count_deals()
    return {"value": total}

# ──────────────── 📅 DATE-RANGE AGGREGATES ────────────
@router.get("/earnings/range", response_model=SimpleFloatOut)
async def earnings_range(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    amount = await AdminDashboard(db).get_sum_earnings_by_date(date_from, date_to)
    return {"value": amount}

@router.get("/credits/range", response_model=SimpleIntOut)
async def credits_range(
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: AsyncSession = Depends(get_async_db),
):
    amount = await AdminDashboard(db).get_sum_credits_by_date(date_from, date_to)
    return {"value": amount}

# ──────────────── 👤 WORKER-BASED ─────────────────────
@router.get("/workers/{worker_id}/clients/new-today", response_model=SimpleIntOut)
async def today_new_clients(worker_id: UUID, db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_sum_today_new_clients(worker_id)
    return {"value": total}
today_new_clients._meta = {"input_model": WorkerIdIn}

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

# ──────────────── BROKER TOTALS ───────────────────────
@router.get("/brokers/clients/signed-count", response_model=SimpleIntOut)
async def signed_by_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_total_count_signed_clients_by_brokers()
    return {"value": total}

@router.get("/brokers/clients/unsigned-count", response_model=SimpleIntOut)
async def unsigned_by_brokers(db: AsyncSession = Depends(get_async_db)):
    total = await AdminDashboard(db).get_total_count_unsigned_clients_by_brokers()
    return {"value": total}

# ──────────────── 📦 BUCKET (PAGINATION) ──────────────
@router.get("/clients", response_model=PaginatedClientsOut)
async def bucket_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    items = await AdminDashboard(db).get_bucket_clients(skip, limit)
    return {"clients": items, "total": len(items)}
bucket_clients._meta = {"input_model": BucketIn}

@router.get("/brokers", response_model=PaginatedBrokersOut)
async def bucket_brokers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    items = await AdminDashboard(db).get_bucket_brokers(skip, limit)
    return {"brokers": items, "total": len(items)}
bucket_brokers._meta = {"input_model": BucketIn}

@router.get("/workers", response_model=PaginatedWorkersOut)
async def bucket_workers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
    db: AsyncSession = Depends(get_async_db),
):
    items = await AdminDashboard(db).get_bucket_workers(skip, limit)
    return {"workers": items, "total": len(items)}
bucket_workers._meta = {"input_model": BucketIn}

# ──────────────── 🔍 SINGLE ENTITIES ──────────────────
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

# ──────────────── 🗑  USER SOFT DELETE ────────────────
@router.patch("/user/{user_id}/deactivate", response_model=StatusMessage)
async def deactivate_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    await AdminDashboard(db).delete_user(user_id)
    return {"status": "deactivated"}

# ──────────────── 🔄 REASSIGNMENT ─────────────────────
@router.patch("/client/{client_id}/assign-worker", response_model=StatusMessage)
async def assign_worker(
    client_id: UUID,
    worker_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).worker_reassign_client(client_id, worker_id)
    return {"status": "reassigned", "worker_id": worker_id}
assign_worker._meta = {"input_model": ClientIdIn}

@router.patch("/client/{client_id}/assign-broker", response_model=StatusMessage)
async def assign_broker(
    client_id: UUID,
    broker_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).broker_reassign_client(client_id, broker_id)
    return {"status": "reassigned", "broker_id": broker_id}
assign_broker._meta = {"input_model": ClientIdIn}

# ──────────────── 💳 CREDIT CONTROL ───────────────────
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

# ──────────────── ✏️ EDIT ENTITIES ───────────────────
@router.patch("/client/{client_id}", response_model=StatusMessage)
async def edit_client(
    client_id: UUID,
    fields: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).edit_client_data(client_id, fields)
    return {"status": "updated"}
edit_client._meta = {"input_model": ClientIdIn}

@router.patch("/broker/{broker_id}", response_model=StatusMessage)
async def edit_broker(
    broker_id: UUID,
    fields: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).edit_broker_data(broker_id, fields)
    return {"status": "updated"}
edit_broker._meta = {"input_model": BrokerIdIn}

@router.patch("/worker/{worker_id}", response_model=StatusMessage)
async def edit_worker(
    worker_id: UUID,
    fields: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_async_db),
):
    await AdminDashboard(db).edit_worker_data(worker_id, fields)
    return {"status": "updated"}
edit_worker._meta = {"input_model": WorkerIdIn}
