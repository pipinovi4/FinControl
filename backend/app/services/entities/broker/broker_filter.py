from sqlalchemy import select, literal
from sqlalchemy.sql import Select
from datetime import datetime

from app.models import Broker
from app.permissions import PermissionRole
from app.services.entities import UserFilterService


class BrokerFilterService(UserFilterService):
    """
    BrokerFilterService builds async-compatible SELECT queries for filtering Brokers.

    Inherits:
        UserFilterService – Provides shared filter logic.

    Public Methods:
        - by_email(email): Filter brokers by partial email match (ILIKE).
        - by_company_name(company): Filter brokers by partial company name.
        - by_display_name(name): Filter by partial Telegram username.
        - by_region(region): Filter brokers that operate in a specific region.
        - by_exact_region_list(regions): Match brokers with exact region list.
        - by_role(role): Filter brokers by role (default: BROKER).
        - by_is_deleted(is_deleted): Filter by soft-deletion status.
        - by_created_after(dt): Filter brokers created after given datetime.
        - by_created_before(dt): Filter brokers created before given datetime.
        - search_email_or_company_name(text): Search by partial match in email or company name.
        - apply(): Finalize and return the composed SQLAlchemy Select query.
    """

    def __init__(self):
        """Initialize the filter service with a base SELECT query."""
        self.query: Select = select(Broker)

    def by_email(self, email: str):
        """
        Filter brokers by email substring (case-insensitive).

        :param email: Email fragment to search for.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.email.ilike(f"%{email}%"))
        return self

    def by_company_name(self, company: str):
        """
        Filter brokers by company name substring (case-insensitive).

        :param company: Company name fragment.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.company_name.ilike(f"%{company}%"))
        return self

    def by_region(self, region: str):
        """
        Filter brokers that operate in a specific region.

        :param region: Region name to match.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.region.any(literal(region)))
        return self

    def by_exact_region_list(self, regions: list[str]):
        """
        Filter brokers that operate in *exact* set of regions (order-insensitive).

        :param regions: List of region names.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.region == regions)
        return self

    def by_role(self, role: PermissionRole = PermissionRole.BROKER):
        """
        Filter brokers by role (default: BROKER).

        :param role: PermissionRole enum value.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.role == role)
        return self

    def by_is_deleted(self, is_deleted: bool = False):
        """
        Filter brokers by soft-deleted status.

        :param is_deleted: Boolean indicating if broker is marked as deleted.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.is_deleted == is_deleted)
        return self

    def by_created_after(self, dt: datetime):
        """
        Filter brokers created after a given datetime.

        :param dt: Datetime to filter from.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.created_at >= dt)
        return self

    def by_created_before(self, dt: datetime):
        """
        Filter brokers created before a given datetime.

        :param dt: Datetime to filter before.
        :return: Self (chainable).
        """
        self.query = self.query.where(Broker.created_at <= dt)
        return self

    def search_email_or_company_name(self, text: str):
        """
        Search brokers by email or company name (case-insensitive).

        :param text: Substring to match against email or company name.
        :return: Self (chainable).
        """
        like = f"%{text}%"
        self.query = self.query.where(
            (Broker.email.ilike(like)) | (Broker.company_name.ilike(like))
        )
        return self

    def apply(self) -> Select:
        """
        Finalize and return the filtered SQLAlchemy Select query.

        :return: A Select query for async execution.
        """
        return self.query
