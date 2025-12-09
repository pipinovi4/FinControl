from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Worker, Application
from app.permissions import PermissionRole


class WorkerFilterService:
    """
    Async service for filtering Worker queries
    in the APPLICATION-based architecture.

    Supports:
        - username / email / role filtering
        - application-based filtering
        - JSONB search inside Application.data
        - count filters (min/max applications)
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.filters = []

    # ---------------------------------------------------------
    # BASIC FIELDS
    # ---------------------------------------------------------
    def by_username(self, username: str):
        self.filters.append(Worker.username == username)
        return self

    def by_email(self, email: str):
        self.filters.append(Worker.email.ilike(f"%{email}%"))
        return self

    def by_role(self):
        """Only WORKER role."""
        self.filters.append(Worker.role == PermissionRole.WORKER)
        return self

    # ---------------------------------------------------------
    # APPLICATION PRESENCE
    # ---------------------------------------------------------
    def by_has_applications(self, has_applications: bool = True):
        """
        True  → workers with ≥1 application
        False → workers with 0 applications
        """
        if has_applications:
            self.filters.append(Worker.applications.any())
        else:
            self.filters.append(~Worker.applications.any())
        return self

    # ---------------------------------------------------------
    # JSONB SEARCH INSIDE Application.data
    # (full_name, phone_number, email)
    # ---------------------------------------------------------
    def by_application_full_name(self, full_name: str):
        self.filters.append(
            Worker.applications.any(
                Application.data["full_name"].astext.ilike(f"%{full_name}%")
            )
        )
        return self

    def by_application_phone_number(self, phone_number: str):
        self.filters.append(
            Worker.applications.any(
                Application.data["phone_number"].astext.ilike(f"%{phone_number}%")
            )
        )
        return self

    def by_application_email(self, email: str):
        self.filters.append(
            Worker.applications.any(
                Application.data["email"].astext.ilike(f"%{email}%")
            )
        )
        return self

    def by_application_id(self, application_id: str):
        self.filters.append(
            Worker.applications.any(Application.id == application_id)
        )
        return self

    # ---------------------------------------------------------
    # COUNT FILTERS
    # ---------------------------------------------------------
    async def by_min_applications_count(self, min_count: int):
        subq = (
            select(Worker.id)
            .join(Application, Worker.id == Application.worker_id)
            .group_by(Worker.id)
            .having(func.count(Application.id) >= min_count)
            .subquery()
        )
        self.filters.append(Worker.id.in_(select(subq.c.id)))
        return self

    async def by_max_applications_count(self, max_count: int):
        subq = (
            select(Worker.id)
            .join(Application, Worker.id == Application.worker_id)
            .group_by(Worker.id)
            .having(func.count(Application.id) <= max_count)
            .subquery()
        )
        self.filters.append(Worker.id.in_(select(subq.c.id)))
        return self

    # ---------------------------------------------------------
    # EXECUTE
    # ---------------------------------------------------------
    async def apply(self):
        stmt = select(Worker).filter(*self.filters)
        result = await self.db.execute(stmt)
        return result.scalars().all()
