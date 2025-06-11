from sqlalchemy.orm import Query
from datetime import datetime
from sqlalchemy import literal

from backend.app.models import Broker
from backend.app.permissions import PermissionRole
from backend.app.services.entities import UserFilterService


class BrokerFilterService(UserFilterService):
    """
    Service for filtering Broker queries based on dynamic conditions.
    """

    def __init__(self, base_query: Query):
        """Initialize the filter service with a base query."""
        super().__init__(base_query)
        self.query = base_query

    def by_email(self, email: str):
        """Filter brokers by email substring (case-insensitive)."""
        self.query = self.query.filter(Broker.email.ilike(f"%{email}%"))
        return self

    def by_company_name(self, company: str):
        """Filter brokers by company name substring (case-insensitive)."""
        self.query = self.query.filter(Broker.company_name.ilike(f"%{company}%"))
        return self

    def by_display_name(self, name: str):
        """Filter brokers by display name substring (case-insensitive)."""
        self.query = self.query.filter(Broker.telegram_username.ilike(f"%{name}%"))
        return self

    def by_region(self, region: str):
        """Filter brokers that operate in a specific region."""
        self.query = self.query.filter(Broker.region.any(literal(region)))
        return self

    def by_exact_region_list(self, regions: list[str]):
        """Filter brokers that operate in *exact* set of regions (order-insensitive)."""
        self.query = self.query.filter(Broker.region == regions)
        return self

    def by_role(self, role: PermissionRole = PermissionRole.BROKER):
        """Filter brokers by role (default: BROKER)."""
        self.query = self.query.filter(Broker.role == role)
        return self

    def by_is_deleted(self, is_deleted: bool = False):
        """Filter brokers by soft-deleted status."""
        self.query = self.query.filter(Broker.is_deleted == is_deleted)
        return self

    def by_created_after(self, dt: datetime):
        """Filter brokers created after a given datetime."""
        self.query = self.query.filter(Broker.created_at >= dt)
        return self

    def by_created_before(self, dt: datetime):
        """Filter brokers created before a given datetime."""
        self.query = self.query.filter(Broker.created_at <= dt)
        return self

    def search_email_or_company_name(self, text: str):
        """Search brokers by email or company name (case-insensitive)."""
        like = f"%{text}%"
        self.query = self.query.filter(
            (Broker.email.ilike(like)) | (Broker.company_name.ilike(like))
        )
        return self

    def apply(self):
        """Finalize and return the filtered query."""
        return self.query
