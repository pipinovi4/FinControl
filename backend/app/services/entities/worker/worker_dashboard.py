from sqlalchemy import (
    select, extract, func, update, and_
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import Any, Sequence
from datetime import datetime, UTC, date, timedelta

from app.models import Application, Credit
from app.schemas.entities.application_schema import (
    WorkerApplicationNewToday,
    ApplicationWorkerOut
)
from app.utils.decorators import handle_exceptions


class WorkerDashboardService:
    """
    Dashboard service rewritten for Application-based architecture.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # -------------------------------------------------------------
    # BASIC COUNTS
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_sum_applications(self, worker_id: UUID) -> int:
        stmt = select(func.count()).select_from(Application).where(
            Application.worker_id == worker_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_total_sum_credits(self, worker_id: UUID) -> float:
        """
        Total credit amount created for worker via Application → Credit.
        """
        stmt = (
            select(func.sum(Credit.amount))
            .join(Application, Application.id == Credit.application_id)
            .where(Application.worker_id == worker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_month_sum_credits(self, worker_id: UUID) -> float:
        now = datetime.now(UTC)
        stmt = (
            select(func.sum(Credit.amount))
            .join(Application, Application.id == Credit.application_id)
            .where(
                Application.worker_id == worker_id,
                extract('year', Credit.issued_at) == now.year,
                extract('month', Credit.issued_at) == now.month,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_sum_deals(self, worker_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Credit)
            .join(Application, Application.id == Credit.application_id)
            .where(Application.worker_id == worker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    # -------------------------------------------------------------
    # NEW APPLICATIONS TODAY / YESTERDAY
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_sum_today_new_applications(self, worker_id: UUID) -> int:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stmt = (
            select(func.count())
            .select_from(Application)
            .where(
                Application.worker_id == worker_id,
                Application.taken_at_worker >= today,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_sum_yesterday_new_applications(self, worker_id: UUID) -> int:
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)

        stmt = (
            select(func.count())
            .select_from(Application)
            .where(
                Application.worker_id == worker_id,
                Application.taken_at_worker >= yesterday,
                Application.taken_at_worker < today,
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_today_new_applications(self, worker_id: UUID) -> list[WorkerApplicationNewToday]:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = (
            select(Application)
            .where(
                Application.worker_id == worker_id,
                Application.taken_at_worker >= today,
            )
        )
        res = await self.db.execute(stmt)
        apps = res.scalars().all()
        return [WorkerApplicationNewToday.model_validate(a) for a in apps]

    # -------------------------------------------------------------
    # PAGINATION
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_bucket_applications(self, worker_id: UUID, skip=0, limit=6):
        stmt = (
            select(Application)
            .where(Application.worker_id == worker_id)
            .order_by(Application.id)
            .offset(skip)
            .limit(limit)
        )
        apps = (await self.db.execute(stmt)).scalars().all()
        return [ApplicationWorkerOut.model_validate(a) for a in apps]

    # -------------------------------------------------------------
    # SINGLE APPLICATION
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_application(self, application_id: UUID):
        stmt = (
            select(Application)
            .where(Application.id == application_id)
            .options(
                selectinload(Application.worker),
                selectinload(Application.broker),
                selectinload(Application.credits),
            )
        )
        result = await self.db.execute(stmt)
        app = result.scalar_one_or_none()
        return ApplicationWorkerOut.model_validate(app) if app else None

    # -------------------------------------------------------------
    # ASSIGN / UNSIGN APPLICATION
    # -------------------------------------------------------------
    @handle_exceptions()
    async def unsign_application(self, application_id: UUID):
        stmt = (
            update(Application)
            .where(Application.id == application_id)
            .values(worker_id=None, taken_at_worker=None)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def sign_application(self, application_id: UUID, worker_id: UUID):
        stmt = (
            update(Application)
            .where(Application.id == application_id)
            .values(worker_id=worker_id, taken_at_worker=datetime.utcnow())
        )
        await self.db.execute(stmt)
        await self.db.commit()

    # -------------------------------------------------------------
    # CREDIT AGGREGATION – MONTH / YEAR
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_credits_for_month(self, worker_id: UUID, month: str):
        year, month_num = map(int, month.split("-"))
        start = date(year, month_num, 1)
        end = date(year + (month_num == 12), (month_num % 12) + 1, 1)

        stmt = (
            select(
                func.date(Credit.issued_at).label("day"),
                func.sum(Credit.amount)
            )
            .join(Application, Application.id == Credit.application_id)
            .where(
                Application.worker_id == worker_id,
                Credit.issued_at >= start,
                Credit.issued_at < end,
            )
            .group_by("day")
        )

        rows = (await self.db.execute(stmt)).all()
        credits_map = {row.day: float(row[1]) for row in rows}

        days = (end - start).days
        return [
            {"date": (start + timedelta(days=i)).isoformat(),
             "amount": round(credits_map.get(start + timedelta(days=i), 0.0), 2)}
            for i in range(days)
        ]

    @handle_exceptions()
    async def get_credits_for_year(self, worker_id: UUID, year: int):
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)

        stmt = (
            select(
                extract("month", Credit.issued_at).label("month"),
                func.sum(Credit.amount)
            )
            .join(Application, Application.id == Credit.application_id)
            .where(
                Application.worker_id == worker_id,
                Credit.issued_at >= start,
                Credit.issued_at < end,
            )
            .group_by("month")
            .order_by("month")
        )

        rows = (await self.db.execute(stmt)).all()
        credits_map = {int(row[0]): float(row[1]) for row in rows}

        return [
            {"month": f"{year}-{m:02}", "amount": round(credits_map.get(m, 0.0), 2)}
            for m in range(1, 12 + 1)
        ]

    # -------------------------------------------------------------
    # ACTIVE / COMPLETED APPLICATIONS
    # -------------------------------------------------------------
    @handle_exceptions()
    async def get_count_completed_applications(self, worker_id: UUID) -> int:
        stmt = (
            select(func.count(Application.id))
            .join(Credit, Application.id == Credit.application_id)
            .where(
                Application.worker_id == worker_id,
                Credit.status == "completed"
            )
            .distinct()
        )
        return (await self.db.execute(stmt)).scalar_one()

    @handle_exceptions()
    async def get_count_active_applications(self, worker_id: UUID) -> int:
        """
        Active = applications without ANY credit.
        """
        stmt = (
            select(func.count(Application.id))
            .outerjoin(Credit, Application.id == Credit.application_id)
            .where(
                Application.worker_id == worker_id,
                Credit.id.is_(None)
            )
        )
        return (await self.db.execute(stmt)).scalar_one()

    # -------------------------------------------------------------
    # FILTER BUCKET APPLICATIONS (JSONB FILTERS!)
    # -------------------------------------------------------------
    @handle_exceptions()
    async def filter_bucket_applications(
        self,
        worker_id: UUID,
        skip=0,
        limit=6,
        *,
        email: str | None = None,
        phone_number: str | None = None,
        full_name: str | None = None,
    ) -> tuple[list[ApplicationWorkerOut], int]:

        filters = [Application.worker_id == worker_id]

        if email:
            filters.append(Application.data["email"].astext.ilike(f"%{email}%"))
        if phone_number:
            filters.append(Application.data["phone_number"].astext.ilike(f"%{phone_number}%"))
        if full_name:
            filters.append(Application.data["full_name"].astext.ilike(f"%{full_name}%"))

        where_clause = and_(*filters)

        # total
        total = (
            await self.db.execute(
                select(func.count()).select_from(Application).where(where_clause)
            )
        ).scalar_one()

        # data
        stmt = (
            select(Application)
            .where(where_clause)
            .order_by(Application.id)
            .offset(skip)
            .limit(limit)
        )

        apps = (await self.db.execute(stmt)).scalars().all()
        return (
            [ApplicationWorkerOut.model_validate(a) for a in apps]