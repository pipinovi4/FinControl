from sqlalchemy import select, func, update, extract, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence, Any
from uuid import UUID
from datetime import datetime, UTC, timedelta, date

from app.models import Client
from app.models.entities.credit import Credit
from app.schemas.entities.client_schema import WorkerClientNewToday, ClientBrokerOut, BrokerClientNewToday
from app.utils.decorators import handle_exceptions


class BrokerDashboard:
    def __init__(self, db: AsyncSession):
        self.db = db

    @handle_exceptions()
    async def get_total_credits_count(self, broker_id: UUID) -> int:
        """
        Return total number of all credits assigned to this broker.
        """
        stmt = select(func.count(Credit.id)).where(Credit.broker_id == broker_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_mount_credits_count(self, broker_id: UUID) -> int:
        """
        Return number of credits issued this month by this broker.
        """
        now = datetime.now(UTC)  # UTC ти вже імпортуєш, нормально

        stmt = (
            select(func.count(Credit.id))
            .where(
                Credit.broker_id == broker_id,
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_count_active_credits(self, broker_id: UUID) -> int:
        """
        Count active credits (status='active') assigned to the broker.
        """
        stmt = (
            select(func.count(Credit.id))
            .where(Credit.broker_id == broker_id, Credit.status == "active")
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_count_completed_credits(self, broker_id: UUID) -> int:
        """
        Count completed credits (status='completed') assigned to the broker.
        """
        stmt = (
            select(func.count(Credit.id))
            .where(Credit.broker_id == broker_id, Credit.status == "closed")
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_sum_signed_clients(self, broker_id: UUID) -> int:
        """
        Count broker's clients that are signed by a worker.
        """
        stmt = (
            select(func.count(Client.id))
            .where(Client.broker_id == broker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_bucket_signed_clients(self, broker_id: UUID, skip: int = 0, limit: int = 8) -> Sequence[Client]:
        """
        Return paginated list of broker's clients that have been signed by a worker.
        """
        stmt = (
            select(Client)
            .where(Client.broker_id == broker_id)
            .order_by(Client.taken_at_broker.asc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Client.worker), selectinload(Client.credits))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def get_bucket_unsigned_clients(self, broker_id: UUID, skip: int = 0, limit: int = 8) -> Sequence[Client]:
        """
        Return paginated list of broker's clients that are not yet signed by a worker.
        """
        stmt = (
            select(Client)
            .where(Client.broker_id == broker_id, Client.worker_id.is_(None))
            .order_by(Client.taken_at_broker.asc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Client.credits))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> ClientBrokerOut | None:
        """
        Get full client info including broker/worker/credits.
        """
        stmt = (
            select(Client)
            .where(Client.id == client_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    @handle_exceptions()
    async def sign_client(self, client_id: UUID, broker_id: UUID) -> None:
        """
        Assign a worker to a broker's client.
        """
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(broker_id=broker_id, taken_at_broker=datetime.utcnow())
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def unsign_client(self, client_id: UUID) -> None:
        """
        Remove worker assignment from a broker's client.
        """
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(broker_id=None, taken_at_broker=None)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    @handle_exceptions()
    async def create_credit(self, client_id: UUID, broker_id: UUID, amount: float) -> Credit:
        """
        Create a credit for a broker's client.
        """
        credit = Credit(client_id=client_id, broker_id=broker_id, amount=amount)
        self.db.add(credit)
        await self.db.commit()
        await self.db.refresh(credit)
        return credit

    @handle_exceptions()
    async def get_sum_today_new_clients(self, broker_id: UUID) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0
                                                )
        stmt = (
            select(func.count())
            .select_from(Client)
            .where(
                Client.broker_id == broker_id,
                Client.taken_at_broker >= today_start,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_sum_yesterday_new_clients(self, broker_id: UUID) -> int:
        now = datetime.utcnow()
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_end = yesterday_start + timedelta(days=1)

        stmt = (
            select(func.count())
            .select_from(Client)
            .where(
                Client.broker_id == broker_id,
                Client.taken_at_broker >= yesterday_start,
                Client.taken_at_broker < yesterday_end,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_today_new_clients(self, broker_id: UUID) -> list[BrokerClientNewToday]:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        stmt = (
            select(Client)
            .where(
                Client.broker_id == broker_id,
                Client.taken_at_broker >= today_start,
            )
        )
        result = await self.db.execute(stmt)
        return [BrokerClientNewToday.model_validate(c) for c in result.scalars().all()]

    @handle_exceptions()
    async def get_sum_broker_commissions(self, broker_id: UUID) -> float:
        """
        Return total sum of worker commissions for this broker's clients.
        """
        stmt = (
            select(func.sum(Credit.amount))
            .join(Client, Client.id == Credit.client_id)
            .where(Client.broker_id == broker_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_month_broker_commissions(self, broker_id: UUID) -> float:
        """
        Return sum of broker commissions for this month, for this broker's clients.
        """
        now = datetime.now(UTC)

        stmt = (
            select(func.sum(Credit.amount))
            .select_from(Credit)
            .join(Client, Client.id == Credit.client_id)
            .where(
                Client.broker_id == broker_id,
                extract("year", Credit.issued_at) == now.year,
                extract("month", Credit.issued_at) == now.month
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_sum_active_credits(self, broker_id: UUID) -> int:
        """
        Sum active credits (status='active') assigned to the broker.
        """
        stmt = (
            select(func.sum(Credit.amount))
            .where(Credit.broker_id == broker_id, Credit.status == "active")
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_sum_completed_credits(self, broker_id: UUID) -> int:
        """
        Sum completed credits (status='completed') assigned to the broker.
        """
        stmt = (
            select(func.sum(Credit.amount))
            .where(Credit.broker_id == broker_id, Credit.status == "closed")
        )
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_credits_for_month(self, broker_id: UUID, month: str) -> list[dict[str, Any]]:
        """
        Return earnings per day for a specific month (YYYY-MM).
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

        # Fetch all earnings in that month
        stmt = (
            select(func.date(Credit.issued_at), func.sum(Credit.amount))
            .where(
                Credit.broker_id == broker_id,
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date,
            )
            .group_by(Credit.issued_at)
        )

        result = await self.db.execute(stmt)
        credits_map = {row[0]: float(row[1]) for row in result.all()}

        # Fill all days with 0 if missing
        total_days = (end_date - start_date).days
        earnings_per_day = []

        for i in range(total_days):
            current_date = start_date + timedelta(days=i)
            earnings_per_day.append({
                "date": current_date.isoformat(),
                "amount": round(credits_map.get(current_date, 0.0), 2)
            })

        return earnings_per_day

    @handle_exceptions()
    async def get_credits_for_year(self, broker_id: UUID, year: int) -> list[dict[str, Any]]:
        """
        Return earnings per month for a specific year.
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
                Credit.broker_id == broker_id,
                Credit.issued_at >= start_date,
                Credit.issued_at < end_date
            )
            .group_by("month")
            .order_by("month")
        )

        result = await self.db.execute(stmt)
        credits_map = {int(row[0]): float(row[1]) for row in result.all()}

        earnings_per_month = []
        for month in range(1, 13):
            earnings_per_month.append({
                "month": f"{year}-{month:02}",
                "amount": round(credits_map.get(month, 0.0), 2)
            })

        return earnings_per_month

    @handle_exceptions()
    async def filter_bucket_clients(
        self,
        broker_id: UUID,
        skip: int = 0,
        limit: int = 6,
        *,
        email: str | None = None,
        phone_number: str | None = None,
        full_name: str | None = None,
    ) -> tuple[list[ClientBrokerOut], int]:
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
            [ClientBrokerOut.model_validate(c) for c in clients],
            total,
        )
