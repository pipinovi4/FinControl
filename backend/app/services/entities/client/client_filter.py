from sqlalchemy import select
from sqlalchemy.sql import Select
from app.models import Client
from app.services.entities.user import UserFilterService


class ClientFilterService(UserFilterService):
    """
    Async-compatible service for dynamically filtering clients using SQLAlchemy Core.

    This service allows for fluent chaining of filter methods and produces an async-friendly
    Select query (to be executed via AsyncSession).

    Filters include:
    - By worker assignment
    - By soft-delete status
    - By credit activity
    - By income range

    Example:
        service = ClientFilterService()
        query = (
            service
            .by_worker(worker_id)
            .by_status(False)
            .by_credit_status(True)
            .apply()
        )
        result = await async_session.execute(query)
        clients = result.scalars().all()
    """

    def __init__(self):
        super().__init__()
        """Initialize with base SELECT query."""
        self.query: Select = select(Client)

    def by_worker(self, worker_id: int):
        """Filter clients by assigned worker."""
        self.query = self.query.where(Client.worker_id == worker_id)
        return self

    def by_status(self, is_deleted: bool):
        """Filter clients by deletion status."""
        self.query = self.query.where(Client.is_deleted == is_deleted)
        return self

    def by_credit_status(self, has_active_credit: bool):
        """Filter clients by active credit status."""
        if has_active_credit:
            self.query = self.query.where(Client.active_credit > 0)
        else:
            self.query = self.query.where(Client.active_credit == 0)
        return self

    def by_income_range(self, min_income: int, max_income: int):
        """Filter clients by income range."""
        self.query = self.query.where(Client.income.between(min_income, max_income))
        return self

    def apply(self) -> Select:
        """Finalize and return the built Select query."""
        return self.query
