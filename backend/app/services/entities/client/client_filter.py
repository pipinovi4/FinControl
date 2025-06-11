from sqlalchemy.orm import Query
from backend.app.models import Client
from backend.app.services.entities import UserFilterService


class ClientFilterService(UserFilterService):
    """
    Service for filtering Client queries based on dynamic conditions.
    """

    def __init__(self, base_query: Query):
        """Initialize the filter service with a base query."""
        super().__init__(base_query)
        self.query = base_query

    def by_worker(self, worker_id: int):
        """Filter clients by assigned worker."""
        self.query = self.query.filter(Client.worker_id == worker_id)
        return self

    def by_status(self, is_deleted: bool):
        """Filter clients by deletion status."""
        self.query = self.query.filter(Client.is_deleted == is_deleted)
        return self

    def by_credit_status(self, has_active_credit: bool):
        """Filter clients by active credit status."""
        if has_active_credit:
            self.query = self.query.filter(Client.active_credit > 0)
        else:
            self.query = self.query.filter(Client.active_credit == 0)
        return self

    def by_income_range(self, min_income: int, max_income: int):
        """Filter clients by income range."""
        self.query = self.query.filter(Client.income.between(min_income, max_income))
        return self

    def apply(self):
        """Finalize and return the query."""
        return self.query