from sqlalchemy import select, extract, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime, UTC, date, timedelta

from backend.app.models import Client
from backend.app.models.entities.earning import Earning
from backend.app.schemas.entities.earning_schema import EarningCreate
from backend.app.utils.decorators import handle_exceptions


class WorkerDashboardService:
    """
    Asynchronous service class responsible for fetching dashboard data
    for a Worker user.

    Provides aggregated information such as:
    - Total number of clients
    - Earnings statistics (monthly, total)
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
    async def get_total_sum_earnings(self, worker_id: UUID) -> float:
        """
        Calculate the total sum of earnings for the given worker.
        """
        stmt = select(func.sum(Earning.amount)).where(Earning.worker_id == worker_id)
        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_month_sum_earnings(self, worker_id: UUID) -> float:
        """
        Calculate the sum of earnings for the current month.
        """
        current_date = datetime.now(UTC)

        stmt = (
            select(func.sum(Earning.amount))
            .where(
                Earning.worker_id == worker_id,
                extract('year', Earning.date) == current_date.year,
                extract('month', Earning.date) == current_date.month,
            )
        )

        result = await self.db.execute(stmt)
        return result.scalar_one() or 0.0

    @handle_exceptions()
    async def get_sum_deals(self, worker_id: UUID) -> int:
        """
        Count total number of deals (earnings entries) for the given worker.
        """
        stmt = (
            select(func.count())
            .select_from(Earning)
            .where(Earning.worker_id == worker_id)
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
    async def get_bucket_clients(
        self,
        worker_id: UUID,
        skip: int = 0,
        limit: int = 8
    ) -> Sequence[Client]:
        """
        Return paginated list of clients assigned to the given worker.

        Args:
            worker_id (UUID): ID of the worker.
            skip (int): Number of records to skip (for pagination).
            limit (int): Maximum number of records to return.

        Returns:
            Sequence[Client]: List of Client objects with related data loaded.
        """
        stmt = (
            select(Client)
            .where(Client.worker_id == worker_id)
            .order_by(Client.created_at.asc())
            .offset(skip)
            .limit(limit)
        )

        # Eager-load related entities to avoid N+1 queries
        stmt = stmt.options(
            selectinload(Client.worker),
            selectinload(Client.broker),
            selectinload(Client.credits)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> Client | None:
        """
        Fetch a single client by their ID, including related entities.

        Args:
            client_id (UUID): ID of the client.

        Returns:
            Client | None: The Client object if found, otherwise None.
        """
        stmt = (
            select(Client)
            .where(Client.id == client_id)
        )

        # Load related worker, broker, and credit information
        stmt = stmt.options(
            selectinload(Client.worker),
            selectinload(Client.broker),
            selectinload(Client.credits)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

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
    async def create_new_earning(self, client_id: UUID, worker_id: UUID, amount: float) -> None:
        """
        Create new record about paying (Earning) for specified client and worker.
        """
        two_months_ago = date.today() - timedelta(days=60)

        earning_data = EarningCreate(
            worker_id=worker_id,
            amount=amount,
            date=two_months_ago,
            client_id=client_id
        )

        earning = Earning(
            client_id=client_id,
            worker_id=earning_data.worker_id,
            date=earning_data.date,
            amount=earning_data.amount,
        )

        self.db.add(earning)
        await self.db.commit()
