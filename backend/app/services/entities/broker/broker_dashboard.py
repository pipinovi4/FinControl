from sqlalchemy import select, func, update, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Sequence
from uuid import UUID
from datetime import datetime, UTC

from backend.app.models import Client
from backend.app.models.entities.credit import Credit
from backend.app.utils.decorators import handle_exceptions


class BrokerDashboard:
    def __init__(self, db: AsyncSession):
        self.db = db

    @handle_exceptions()
    async def get_total_credits_sum(self, broker_id: UUID) -> int:
        """
        Return total number of all credits assigned to this broker.
        """
        stmt = select(func.count(Credit.id)).where(Credit.broker_id == broker_id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    @handle_exceptions()
    async def get_mount_credits_sum(self, broker_id: UUID) -> int:
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
    async def get_sum_active_credits(self, broker_id: UUID) -> int:
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
    async def get_sum_completed_credits(self, broker_id: UUID) -> int:
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
            .where(Client.broker_id == broker_id, Client.worker_id.is_not(None))
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
            .where(Client.broker_id == broker_id, Client.worker_id.is_not(None))
            .order_by(Client.created_at.asc())
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
            .order_by(Client.created_at.asc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Client.credits))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    @handle_exceptions()
    async def get_client(self, client_id: UUID) -> Client | None:
        """
        Get full client info including broker/worker/credits.
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
        return result.scalar_one_or_none()

    @handle_exceptions()
    async def sign_client(self, client_id: UUID, worker_id: UUID) -> None:
        """
        Assign a worker to a broker's client.
        """
        stmt = (
            update(Client)
            .where(Client.id == client_id)
            .values(broker_id=worker_id, taken_at_worker=datetime.utcnow())
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
            .values(worker_id=None, taken_at_worker=None)
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    @handle_exceptions()
    async def create_credit(self, client_id: UUID, broker_id: UUID, amount: int) -> Credit:
        """
        Create a credit for a broker's client.
        """
        credit = Credit(client_id=client_id, broker_id=broker_id, amount=amount)
        self.db.add(credit)
        await self.db.commit()
        await self.db.refresh(credit)
        return credit