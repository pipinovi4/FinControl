from __future__ import annotations

from datetime import datetime, UTC, date
from typing import Sequence, Any, Mapping

from sqlalchemy import (
    select,
    func,
    extract,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID

from backend.app.models import Client, Broker, Worker, Admin, User
from backend.app.models.entities.credit import Credit
from backend.app.models.entities.earning import Earning
from backend.app.utils.decorators import handle_exceptions


class AdminDashboard:
    """
    High-level service for global analytics & administration.
    Works on *all* users, credits, earnings.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ─────────────────────────────
    # 📊 GLOBAL AGGREGATES
    # ─────────────────────────────

    @handle_exceptions()
    async def get_total_sum_earnings(self) -> float:
        """Total amount of all workers’ earnings."""
        stmt = select(func.coalesce(func.sum(Earning.amount), 0.0))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_sum_credits(self) -> int:
        """Total *nominal* volume of credits (sum of total_amount)."""
        stmt = select(func.coalesce(func.sum(Credit.amount), 0))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_month_sum_earnings(self) -> float:
        """Earnings paid this month (all workers)."""
        now = datetime.now(UTC)
        stmt = (
            select(func.coalesce(func.sum(Earning.amount), 0.0))
            .where(
                extract("year", Earning.date) == now.year,
                extract("month", Earning.date) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_month_sum_credits(self) -> int:
        """Credits *issued* this month (sum total_amount)."""
        now = datetime.now(UTC)
        stmt = (
            select(func.coalesce(func.sum(Credit.amount), 0))
            .where(
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_clients(self) -> int:
        """How many clients exist (not soft-deleted)."""
        stmt = select(func.count(Client.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_brokers(self) -> int:
        """How many brokers exist."""
        stmt = select(func.count(Broker.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_credits(self) -> int:
        """Count of credit contracts rows."""
        stmt = select(func.count(Credit.id))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_deals(self) -> int:
        """Count of individual earning entries (deals)."""
        stmt = select(func.count(Earning.id))
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 📅 DATE-RANGE AGGREGATES
    # ─────────────────────────────

    @handle_exceptions()
    async def get_sum_earnings_by_date(
        self, date_from: date, date_to: date
    ) -> float:
        """Sum of earnings in arbitrary period [date_from; date_to]."""
        stmt = (
            select(func.coalesce(func.sum(Earning.amount), 0.0))
            .where(Earning.date.between(date_from, date_to))
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_credits_by_date(
        self, date_from: date, date_to: date
    ) -> int:
        """Sum of credit totals issued in period."""
        stmt = (
            select(func.coalesce(func.sum(Credit.total_amount), 0))
            .where(Credit.issued_at.between(date_from, date_to))
        )
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 🔎 TODAY / PER-WORKER
    # ─────────────────────────────

    @handle_exceptions()
    async def get_sum_today_new_clients(self, worker_id: UUID) -> int:
        """Clients taken *today* by given worker."""
        start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count())
            .select_from(Client)
            .where(Client.worker_id == worker_id, Client.taken_at_worker >= start)
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_signed_clients_by_worker(self, worker_id: UUID) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id == worker_id)
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_unsigned_clients_by_worker(self) -> int:
        stmt = (
            select(func.count(Client.id))
            .where(Client.worker_id.is_(None))
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_count_signed_clients_by_brokers(self) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id.isnot(None))
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_total_count_unsigned_clients_by_brokers(self) -> int:
        stmt = select(func.count(Client.id)).where(Client.worker_id.is_(None))
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────
    # 📦 BUCKET (PAGINATION)
    # ─────────────────────────────

    async def _bucket(
        self,
        model,
        skip: int = 0,
        limit: int = 20,
        *options,
    ) -> Sequence[Any]:
        stmt = (
            select(model)
            .order_by(model.created_at.desc())
            .offset(skip)
            .limit(limit)
        ).options(*options)
        return (await self.db.execute(stmt)).scalars().all()

    @handle_exceptions()
    async def get_bucket_clients(
        self, skip: int = 0, limit: int = 20
    ) -> Sequence[Client]:
        return await self._bucket(
            Client,
            skip,
            limit,
            selectinload(Client.worker),
            selectinload(Client.broker),
            selectinload(Client.credits),
        )

    @handle_exceptions()
    async def get_bucket_brokers(
        self, skip: int = 0, limit: int = 20
    ) -> Sequence[Broker]:
        return await self._bucket(Broker, skip, limit, selectinload(Broker.clients), selectinload(Broker.credits))

    @handle_exceptions()
    async def get_bucket_workers(
        self, skip: int = 0, limit: int = 20
    ) -> Sequence[Worker]:
        return await self._bucket(Worker, skip, limit, selectinload(Worker.clients), selectinload(Worker.earnings))

    # ─────────────────────────────
    # 🔍 SINGLE-ENTITY FETCH
    # ─────────────────────────────

    async def _get_one(self, model, entity_id: UUID, *options):
        stmt = select(model).where(model.id == entity_id).options(*options)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> Client | None:
        return await self._get_one(
            Client,
            client_id,
            selectinload(Client.worker),
            selectinload(Client.broker),
            selectinload(Client.credits),
        )

    @handle_exceptions()
    async def get_worker(self, worker_id: UUID) -> Worker | None:
        return await self._get_one(
            Worker,
            worker_id,
            selectinload(Worker.clients),
            selectinload(Worker.earnings),
        )

    @handle_exceptions()
    async def get_broker(self, broker_id: UUID) -> Broker | None:
        return await self._get_one(
            Broker,
            broker_id,
            selectinload(Broker.clients),
        )

    # ─────────────────────────────
    # 🛠 ADMIN ACTIONS
    # ─────────────────────────────

    @handle_exceptions()
    async def delete_user(self, user_id: UUID) -> None:
        """Soft-delete (is_active=False) any user."""
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    # ── REASSIGNMENT ────────────────────

    @handle_exceptions()
    async def worker_reassign_client(
        self, client_id: UUID, new_worker_id: UUID | None
    ) -> None:
        """
        Assign or unassign a worker for given client.
        If `new_worker_id` is None → unassign.
        """
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(
                worker_id=new_worker_id,
                taken_at_worker=datetime.now(UTC) if new_worker_id else None,
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    @handle_exceptions()
    async def broker_reassign_client(
        self, client_id: UUID, new_broker_id: UUID | None
    ) -> None:
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(
                broker_id=new_broker_id,
                taken_at_broker=datetime.now(UTC) if new_broker_id else None,
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    # ── CREDIT CONTROL ─────────────────

    @handle_exceptions()
    async def force_complete_credit(self, credit_id: UUID) -> None:
        """
        Mark credit as fully paid (paid_amount=total_amount, status='completed').
        """
        stmt = (
            update(Credit)
            .where(Credit.id == credit_id)
            .values(
                paid_amount=Credit.total_amount,
                status="completed",
                last_payment_at=datetime.now(UTC),
            )
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    @handle_exceptions()
    async def change_credit_status(
        self, credit_id: UUID, new_status: str
    ) -> None:
        stmt = (
            update(Credit)
            .where(Credit.id == credit_id)
            .values(status=new_status)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    # ── EDIT DATA HELPERS ───────────────
    # (expect `fields` as mapping of column names -> values)

    async def _edit_entity(
        self, model, entity_id: UUID, fields: Mapping[str, Any]
    ) -> None:
        if not fields:
            return
        stmt = (
            update(model)
            .where(model.id == entity_id)
            .values(**fields)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    @handle_exceptions()
    async def edit_client_data(
        self, client_id: UUID, fields: Mapping[str, Any]
    ) -> None:
        await self._edit_entity(Client, client_id, fields)

    @handle_exceptions()
    async def edit_broker_data(
        self, broker_id: UUID, fields: Mapping[str, Any]
    ) -> None:
        await self._edit_entity(Broker, broker_id, fields)

    @handle_exceptions()
    async def edit_worker_data(
        self, worker_id: UUID, fields: Mapping[str, Any]
    ) -> None:
        await self._edit_entity(Worker, worker_id, fields)
