from __future__ import annotations
from datetime import datetime, UTC, timedelta, date
from typing import Sequence, Any
from uuid import UUID

from sqlalchemy import (
    select, func, update, extract, and_, or_
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.entities.application import Application
from app.models.entities.credit import Credit, CreditStatus
from app.schemas.entities.application_schema import (
    BrokerApplicationNewToday,
    ApplicationAdminOut,
)
from app.utils.decorators import handle_exceptions


class BrokerDashboard:
    """
    NEW VERSION — broker dashboard works ONLY with APPLICATION.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ─────────────────────────────────────────
    # 📌 BASIC CREDIT METRICS
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_total_credits_count(self, broker_id: UUID) -> int:
        stmt = select(func.count(Credit.id)).where(Credit.broker_id == broker_id)
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_month_credits_count(self, broker_id: UUID) -> int:
        now = datetime.now(UTC)
        stmt = (
            select(func.count(Credit.id))
            .where(
                Credit.broker_id == broker_id,
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_active_credits(self, broker_id: UUID) -> int:
        stmt = (
            select(func.count(Credit.id))
            .where(
                Credit.broker_id == broker_id,
                Credit.status != CreditStatus.COMPLETED,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_completed_credits(self, broker_id: UUID) -> int:
        stmt = (
            select(func.count(Ccredit.id))
            .where(
                Credit.broker_id == broker_id,
                Credit.status == CreditStatus.COMPLETED,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────────────────
    # 📌 APPLICATIONS STAT
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_sum_signed_applications(self, broker_id: UUID) -> int:
        stmt = select(func.count(Application.id)).where(
            Application.broker_id == broker_id
        )
        return (await self.db.execute(stmt)).scalar_one()

    # ─────────────────────────────────────────
    # 📦 PAGINATED LISTS
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_bucket_signed_applications(
        self, broker_id: UUID, skip: int = 0, limit: int = 8
    ) -> Sequence[Application]:
        """
        Applications that HAVE broker assigned.
        """
        stmt = (
            select(Application)
            .where(Application.broker_id == broker_id)
            .order_by(Application.taken_at_broker.asc())
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Application.worker),
                selectinload(Application.credits),
            )
        )
        return (await self.db.execute(stmt)).scalars().all()

    @handle_exceptions()
    async def get_bucket_unsigned_applications(
        self, broker_id: UUID, skip: int = 0, limit: int = 8
    ) -> Sequence[Application]:
        """
        Applications WITHOUT worker assigned yet.
        """
        stmt = (
            select(Application)
            .where(
                Application.broker_id == broker_id,
                Application.worker_id.is_(None),
            )
            .order_by(Application.taken_at_broker.asc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Application.credits))
        )
        return (await self.db.execute(stmt)).scalars().all()

    # ─────────────────────────────────────────
    # 📌 SINGLE APPLICATION
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_application(self, app_id: UUID) -> ApplicationAdminOut | None:
        stmt = (
            select(Application)
            .where(Application.id == app_id)
            .options(
                selectinload(Application.worker),
                selectinload(Application.broker),
                selectinload(Application.credits),
            )
        )
        app = (await self.db.execute(stmt)).scalar_one_or_none()
        if not app:
            return None
        return ApplicationAdminOut.model_validate(app)

    # ─────────────────────────────────────────
    # ASSIGN / UNASSIGN
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def assign_application(self, app_id: UUID, broker_id: UUID) -> None:
        """
        Broker takes an application.
        """
        await self.db.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(
                broker_id=broker_id,
                taken_at_broker=datetime.utcnow(),
            )
        )
        await self.db.commit()

    @handle_exceptions()
    async def unassign_application(self, app_id: UUID) -> None:
        """
        Remove broker from application.
        """
        await self.db.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(
                broker_id=None,
                taken_at_broker=None,
            )
        )
        await self.db.commit()

    # ─────────────────────────────────────────
    # CREATE CREDIT FROM APPLICATION
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def create_credit(self, app_id: UUID, broker_id: UUID, amount: float) -> Credit:
        credit = Credit(
            application_id=app_id,
            broker_id=broker_id,
            amount=amount,
        )
        self.db.add(credit)
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    # ─────────────────────────────────────────
    # TODAY / YESTERDAY NEW APPS
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_sum_today_new_applications(self, broker_id: UUID) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count(Application.id))
            .where(
                Application.broker_id == broker_id,
                Application.taken_at_broker >= today_start,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_yesterday_new_applications(self, broker_id: UUID) -> int:
        now = datetime.utcnow()
        y_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        y_end   = y_start + timedelta(days=1)

        stmt = (
            select(func.count(Application.id))
            .where(
                Application.broker_id == broker_id,
                Application.taken_at_broker >= y_start,
                Application.taken_at_broker < y_end,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_today_new_applications(self, broker_id: UUID) -> list[BrokerApplicationNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = (
            select(Application)
            .where(
                Application.broker_id == broker_id,
                Application.taken_at_broker >= today_start,
            )
        )
        apps = (await self.db.execute(stmt)).scalars().all()
        return [BrokerApplicationNewToday(id=a.id, taken_at_broker=a.taken_at_broker) for a in apps]

    # ─────────────────────────────────────────
    # COMMISSIONS
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_sum_broker_commissions(self, broker_id: UUID) -> float:
        stmt = (
            select(func.sum(Credit.amount))
            .where(Credit.broker_id == broker_id)
        )
        return (await self.db.execute(stmt)).scalar_one() or 0.0

    @handle_exceptions()
    async def get_month_broker_commissions(self, broker_id: UUID) -> float:
        now = datetime.now(UTC)
        stmt = (
            select(func.sum(Credit.amount))
            .where(
                Credit.broker_id == broker_id,
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month,
            )
        )
        return (await self.db.execute(stmt)).scalar_one() or 0.0

    # ─────────────────────────────────────────
    # MONTHLY BY DAYS
    # ─────────────────────────────────────────
    @handle_exceptions()
    async def get_credits_for_month(self, broker_id: UUID, month: str) -> list[dict[str, Any]]:
        try:
            year, m = map(int, month.split("-"))
            start_date = date(year, m, 1)
            end_date   = date(year + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
        except Exception:
            raise ValueError("Invalid month format: YYYY-MM required")

        stmt = (
            select(
                func.date(Credit.issued_at).label("day"),
                func.sum(Credit.amount).label("total"),
            )
            .where(
                Credit.broker_id == broker_id,
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date,
            )
            .group_by(func.date(Credit.issued_at))
            .order_by(func.date(Credit.issued_at))
        )

        rows = (await self.db.execute(stmt)).all()
        totals = {day: total for day, total in rows}

        out = []
        for i in range((end_date - start_date).days):
            d = start_date + timedelta(days=i)
            out.append({
                "date": d.isoformat(),
                "amount": float(totals.get(d, 0.0)),
            })

        return out
