from sqlalchemy.orm import Query
from sqlalchemy import func
from datetime import datetime
from backend.app.models import Worker, Client
from backend.app.permissions import PermissionRole
from backend.app.services.entities import UserFilterService


class WorkerFilterService(UserFilterService):
    """
    Service for filtering Worker queries based on dynamic conditions.
    """

    def __init__(self, base_query: Query):
        """
        Initialize the filter service with a base query.
        :param base_query: Initial SQLAlchemy Query object.
        """
        super().__init__(base_query)
        self.query = base_query

    def by_username(self, username: str):
        """
        Filter workers by the system username.
        :param username: The worker's username.
        """
        self.query = self.query.filter(Worker.username == username)
        return self

    def by_telegram_username(self, telegram_username: str):
        """
        Filter workers by Telegram username.
        :param telegram_username: The Telegram handle.
        """
        self.query = self.query.filter(Worker.telegram_username == telegram_username)
        return self

    def by_email(self, email: str):
        """
        Filter workers by email (from AuthMixin).
        :param email: The email substring to search for.
        """
        self.query = self.query.filter(Worker.email.ilike(f"%{email}%"))
        return self

    def by_has_clients(self, has_clients: bool = True):
        """
        Filter workers based on whether they have assigned clients.
        If it has_clients is True, returns workers with at least one client;
        if False, returns workers with no assigned clients.
        """
        if has_clients:
            self.query = self.query.filter(Worker.clients.any())
        else:
            self.query = self.query.filter(~Worker.clients.any())
        return self

    def by_min_clients_count(self, min_count: int):
        """
        Filter workers who have at least `min_count` clients assigned.
        This uses a subquery with a join and group_by.
        :param min_count: Minimum number of clients.
        """
        subq = (
            self.query.session.query(Worker.id, func.count(Client.id).label("client_count"))
            .join(Worker.clients)
            .group_by(Worker.id)
            .subquery()
        )
        self.query = self.query.join(subq, Worker.id == subq.c.id).filter(subq.c.client_count >= min_count)
        return self

    def by_max_clients_count(self, max_count: int):
        """
        Filter workers who have at most `max_count` clients assigned.
        :param max_count: Maximum number of clients.
        """
        subq = (
            self.query.session.query(Worker.id, func.count(Client.id).label("client_count"))
            .join(Worker.clients)
            .group_by(Worker.id)
            .subquery()
        )
        self.query = self.query.join(subq, Worker.id == subq.c.id).filter(subq.c.client_count <= max_count)
        return self

    def by_role(self):
        """
        Filter workers by role.
        Assumes that Worker.role exists and that PermissionRole.WORKER represents the worker role.
        """
        self.query = self.query.filter(Worker.role == PermissionRole.WORKER)
        return self

    # --- Фільтри за даними клієнтів, які менеджер має ---

    def by_client_full_name(self, full_name: str):
        """
        Filter workers by the full name of at least one of their clients.
        Checks if any assigned client's full_name contains the substring (case-insensitive).

        :param full_name: Substring to search within client's full_name.
        """
        self.query = self.query.filter(Worker.clients.any(Client.full_name.ilike(f"%{full_name}%")))
        return self

    def by_client_phone_number(self, phone_number: str):
        """
        Filter workers by a client's phone number.
        Checks if any assigned client's phone number contains the given substring.

        :param phone_number: Substring to search within client's phone number.
        """
        self.query = self.query.filter(Worker.clients.any(Client.phone_number.ilike(f"%{phone_number}%")))
        return self

    def by_client_email(self, email: str):
        """
        Filter workers by a client's email address.
        Checks if any assigned client's email contains the given substring.

        :param email: Substring to search within client's email.
        """
        self.query = self.query.filter(Worker.clients.any(Client.email.ilike(f"%{email}%")))
        return self

    def by_client_id(self, client_id: str):
        """
        Filter workers by a specific client ID.
        Checks if any assigned client's id equals the provided client_id.

        :param client_id: The UUID (as string) of the client.
        """
        self.query = self.query.filter(Worker.clients.any(Client.id == client_id))
        return self

    def apply(self):
        """
        Finalize and return the filtered query.
        :return: The SQLAlchemy Query object with all applied filters.
        """
        return self.query