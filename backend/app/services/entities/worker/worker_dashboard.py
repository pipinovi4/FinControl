from sqlalchemy import select, extract, func, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Sequence
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime, UTC, date, timedelta

from backend.app.models import Client, Credit
from backend.app.schemas.entities.client_schema import WorkerClientNewToday, ClientWorkerOut
from backend.app.schemas.entities.credit_schema import CreditCreate
from backend.app.utils.decorators import handle_exceptions


class WorkerDashboardService:
    """
    Asynchronous service class responsible for fetching dashboard data
    for a Worker user.

    Provides aggregated information such as:
    - Total number of clients
    - Credits statistics (monthly, total)
    - New clients today
    - Paginated client lists
    - Detailed client info
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the service with an async database session.
        """
        self.db = db

    @handle_exceptions()
    async def get_sum_clients(self, worker_id: UUID) -> int:
        """
        Count total number of clients assigned to the given worker.
        """
        stmt = (
            select(func.count())
            .select_from(Client)
            .where(Client.worker_id == worker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_total_sum_credits(self, worker_id: UUID) -> float:
        """
        Calculate the total sum of credits for the given worker.
        """
        stmt = select(func.sum(Credit.amount)).where(Credit.worker_id == worker_id)
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_month_sum_credits(self, worker_id: UUID) -> float:
        """
        Calculate the sum of credits for the current month.
        """
        current_date = datetime.now(UTC)

        stmt = (
            select(func.sum(Credit.amount))
            .where(
                Credit.worker_id == worker_id,
                extract('year', Credit.issued_at) == current_date.year,
                extract('month', Credit.issued_at) == current_date.month,
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_sum_deals(self, worker_id: UUID) -> int:
        """
        Count total number of deals (credits entries) for the given worker.
        """
        stmt = (
            select(func.count())
            .select_from(Credit)
            .where(Credit.worker_id == worker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    @handle_exceptions()
    async def get_sum_today_new_clients(self, worker_id: UUID) -> int:
        """
        Count number of clients taken by the worker today.
        """
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = (
            select(func.count())
            .select_from(Client)
            .where(
                Client.worker_id == worker_id,
                Client.taken_at_worker >= today_start,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    @handle_exceptions()
    async def get_sum_yesterday_new_clients(self, worker_id: UUID) -> int:
        """
        Count a number of clients taken by the worker yesterday.
        """
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)

        stmt = (
            select(func.count())
            .select_from(Client)
            .where(
                Client.worker_id == worker_id,
                Client.taken_at_worker >= yesterday_start,
                Client.taken_at_worker < today_start,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0

    @handle_exceptions()
    async def get_today_new_clients(self, worker_id: UUID) -> list[WorkerClientNewToday]:
        """
        Return list of clients taken by the worker today.
        """
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = (
            select(Client)
            .where(
                Client.worker_id == worker_id,
                Client.taken_at_worker >= today_start,
            )
        )
        result = await self.db.execute(stmt)
        return [WorkerClientNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_bucket_clients(
            self,
            worker_id: UUID,
            skip: int = 0,
            limit: int = 6,
    ) -> list[ClientWorkerOut]:
        """
        Return paginated and validated list of clients for a worker.
        """
        stmt = (
            select(Client)
            .where(Client.worker_id == worker_id)
            .order_by(Client.id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        clients = result.scalars().all()
        return [ClientWorkerOut.model_validate(c) for c in clients]

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> ClientWorkerOut | None:
        """
        Fetch and validate a single client by ID.
        """
        stmt = (
            select(Client)
            .where(Client.id == client_id)
            .options(
                selectinload(Client.worker),
                selectinload(Client.broker),
                selectinload(Client.credits)
            )
        )

        result = await self.db.execute(stmt)
        client = result.scalar_one_or_none()

        return ClientWorkerOut.model_validate(client) if client else None

    @handle_exceptions()
    async def unsign_client(self, client_id: UUID) -> None:
        """
        Unsign a client from their current worker.
        """
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(worker_id=None, taken_at_worker=None)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def sign_client(self, client_id: UUID, worker_id: UUID) -> None:
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(worker_id=worker_id, taken_at_worker=datetime.utcnow())
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def get_credits_for_month(self, worker_id: UUID, month: str) -> list[dict[str, Any]]:
        """
        Return credits per day for a specific month (YYYY-MM).
        """
        try:
            year, month_num = map(int, month.split("-"))
            start_date = date(year, month_num, 1)
            if month_num == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year, month_num + 1, 1)
        except Exception:
            raise ValueError("Invalid month format. Expected YYYY-MM.")

        # Fetch all credits in that month
        stmt = (
            select(Credit.issued_at, func.sum(Credit.amount))
            .where(
                Credit.worker_id == worker_id,
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date,
            )
            .group_by(Credit.issued_at)
        )

        result = await self.db.execute(stmt)
        credits_map = {row.date: float(row[1]) for row in result.all()}

        # Fill all days with 0 if missing
        total_days = (end_date - start_date).days
        credits_per_day = []

        for i in range(total_days):
            current_date = start_date + timedelta(days=i)
            credits_per_day.append({
                "date": current_date.isoformat(),
                "amount": round(credits_map.get(current_date, 0.0), 2)
            })

        return credits_per_day

    @handle_exceptions()
    async def get_credits_for_year(self, worker_id: UUID, year: int) -> list[dict[str, Any]]:
        """
        Return credits per month for a specific year.
        """
        # ⛔ safety check
        if year < 1900:
            raise ValueError("Invalid year format. Must be 4 digits, e.g. 2025")

        start_date = date(year, 1, 1)
        end_date = date(year + 1, 1, 1)

        stmt = (
            select(
                extract("month", Credit.issued_at).label("month"),
                func.sum(Credit.amount)
            )
            .where(
                Credit.worker_id == worker_id,
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date
            )
            .group_by("month")
            .order_by("month")
        )

        result = await self.db.execute(stmt)
        credits_map = {int(row[0]): float(row[1]) for row in result.all()}

        credits_per_month = []
        for month in range(1, 13):
            credits_per_month.append({
                "month": f"{year}-{month:02}",
                "amount": round(credits_map.get(month, 0.0), 2)
            })

        return credits_per_month

    @handle_exceptions()
    async def get_count_completed_clients(self, worker_id: UUID) -> int:
        stmt = (
            select(func.count(Client.id))
            .join(Credit, Client.id == Credit.client_id)
            .where(
                Client.worker_id == worker_id,
                Credit.status == "completed")
            .distinct()
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_count_active_clients(self, worker_id: UUID) -> int:
        stmt = (
            select(func.count(Client.id))
            .outerjoin(Credit, Client.id == Credit.client_id)
            .where(
                Client.worker_id == worker_id,
                Credit.id.is_(None)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def filter_bucket_clients(
        self,
        worker_id: UUID,
        skip: int = 0,
        limit: int = 6,
        *,
        email: str | None = None,
        phone_number: str | None = None,
        full_name: str | None = None,
    ) -> tuple[list[ClientWorkerOut], int]:
        """
        Вернуть (список, total) клиентов конкретного работника,
        удовлетворяющих переданным фильтрам, с пагинацией.
        """

        # ------- динамический WHERE ---------------------------------
        conditions = []

        if email:
            conditions.append(Client.email.ilike(f"%{email}%"))
        if phone_number:
            conditions.append(Client.phone_number.ilike(f"%{phone_number}%"))
        if full_name:
            conditions.append(Client.full_name.ilike(f"%{full_name}%"))

        where_clause = and_(*conditions)

        # ------- total ----------------------------------------------
        total_stmt = select(func.count()).select_from(Client).where(where_clause)
        total_res  = await self.db.execute(total_stmt)
        total: int = total_res.scalar_one()

        # ------- данные страницы ------------------------------------
        data_stmt = (
            select(Client)
            .where(where_clause)
            .options(
                selectinload(Client.worker),
                selectinload(Client.broker),
                selectinload(Client.credits),
            )
            .order_by(Client.full_name.asc())
            .offset(skip)
            .limit(limit)
        )

        data_res = await self.db.execute(data_stmt)
        clients: Sequence[Client] = data_res.scalars().all()

        return (
            [ClientWorkerOut.model_validate(c) for c in clients],
            total,
        )
