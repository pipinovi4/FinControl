from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.models import Worker, Client
from backend.app.permissions import PermissionRole


class WorkerFilterService:
    """
    Async service for filtering Worker queries based on dynamic conditions.

    Methods:
        - by_username(username): Filter workers by their system username.
        - by_telegram_username(telegram_username): Filter by Telegram username.
        - by_email(email): Filter workers by email address (partial match).
        - by_has_clients(has_clients): Filter workers based on presence of assigned clients.
        - by_role(): Filter only users with WORKER role.
        - by_client_full_name(full_name): Filter if worker has client with matching name.
        - by_client_phone_number(phone_number): Filter if worker has client with matching phone.
        - by_client_email(email): Filter if worker has client with matching email.
        - by_client_id(client_id): Filter if worker has client with specific ID.
        - by_min_clients_count(min_count): Filter workers who have at least X clients.
        - by_max_clients_count(max_count): Filter workers who have at most X clients.
        - apply(): Executes the query and returns matching Worker instances.
    """
    def __init__(self, db: AsyncSession):
        """
        Initialize the filter service with a database session.
        :param db: Async SQLAlchemy session.
        """
        self.db = db
        self.filters = []

    def by_username(self, username: str):
        """
        Filter workers by the system username.
        """
        self.filters.append(Worker.username == username)
        return self

    def by_telegram_username(self, telegram_username: str):
        """
        Filter workers by Telegram username.
        """
        self.filters.append(Worker.telegram_username == telegram_username)
        return self

    def by_email(self, email: str):
        """
        Filter workers by email address.
        Uses a case-insensitive LIKE match.
        """
        self.filters.append(Worker.email.ilike(f"%{email}%"))
        return self

    def by_has_clients(self, has_clients: bool = True):
        """
        Filter workers based on whether they have assigned clients.
        If has_clients is True — only workers with clients.
        If has_clients is False — only workers without clients.
        """
        if has_clients:
            self.filters.append(Worker.clients.any())
        else:
            self.filters.append(~Worker.clients.any())
        return self

    def by_role(self):
        """
        Filter workers by role.
        Only includes users with PermissionRole.WORKER.
        """
        self.filters.append(Worker.role == PermissionRole.WORKER)
        return self

    def by_client_full_name(self, full_name: str):
        """
        Filter workers by presence of a client with matching full name.
        Case-insensitive partial match.
        """
        self.filters.append(Worker.clients.any(Client.full_name.ilike(f"%{full_name}%")))
        return self

    def by_client_phone_number(self, phone_number: str):
        """
        Filter workers by presence of a client with matching phone number.
        """
        self.filters.append(Worker.clients.any(Client.phone_number.ilike(f"%{phone_number}%")))
        return self

    def by_client_email(self, email: str):
        """
        Filter workers by presence of a client with matching email.
        """
        self.filters.append(Worker.clients.any(Client.email.ilike(f"%{email}%")))
        return self

    def by_client_id(self, client_id: str):
        """
        Filter workers by presence of a client with the given ID.
        """
        self.filters.append(Worker.clients.any(Client.id == client_id))
        return self

    async def by_min_clients_count(self, min_count: int):
        """
        Filter workers who have at least `min_count` clients assigned.
        Uses a subquery with GROUP BY and HAVING clause.
        """
        subq = (
            select(Worker.id, func.count(Client.id).label("client_count"))
            .join(Client, Worker.id == Client.worker_id)
            .group_by(Worker.id)
            .having(func.count(Client.id) >= min_count)
            .subquery()
        )
        self.filters.append(Worker.id.in_(select(subq.c.id)))
        return self

    async def by_max_clients_count(self, max_count: int):
        """
        Filter workers who have at most `max_count` clients assigned.
        Uses a subquery with GROUP BY and HAVING clause.
        """
        subq = (
            select(Worker.id, func.count(Client.id).label("client_count"))
            .join(Client, Worker.id == Client.worker_id)
            .group_by(Worker.id)
            .having(func.count(Client.id) <= max_count)
            .subquery()
        )
        self.filters.append(Worker.id.in_(select(subq.c.id)))
        return self

    async def apply(self):
        """
        Finalize and execute the built query.
        Returns a list of Worker instances matching the accumulated filters.
        """
        stmt = select(Worker).filter(*self.filters)
        result = await self.db.execute(stmt)
        return result.scalars().all()
