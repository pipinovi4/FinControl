from typing import TypeVar

from app.models import Broker
from app.services.entities import UserInterfaceService

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerInterfaceService(UserInterfaceService):
    """
    High-level interface wrapper for Broker entity.

    After migration to Application-based architecture:
      - brokers don't have `.applications`
      - they DO have `.applications`

    This interface provides:
        - company display logic
        - region access helpers
        - application count helpers
        - active/deleted status helpers
        - safe field access
    """

    def __init__(self, broker: BrokerT):
        super().__init__(broker)
        self.broker: BrokerT = broker

    # ---------------------------------------------------------
    # BASIC ACCESSORS
    # ---------------------------------------------------------
    def get_display_name(self) -> str:
        """Return broker’s company name or fallback like Broker#abc123."""
        return self.broker.company_name or f"Broker#{str(self.broker.id)[:6]}"

    def get_email(self) -> str:
        """Return broker’s email (stringified to avoid None)."""
        return str(self.broker.email or "")

    def get_regions(self) -> list[str]:
        """Return list of broker’s regions."""
        return self.broker.region or []

    # ---------------------------------------------------------
    # APPLICATION COUNTS (REPLACING OLD APPLICATIONS)
    # ---------------------------------------------------------
    def get_applications_count(self) -> int:
        """Return number of Applications assigned to the broker."""
        return len(self.broker.applications or [])

    def has_applications(self) -> bool:
        """Return True if the broker has at least one Application."""
        return bool(self.broker.applications)

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------
    def is_active(self) -> bool:
        """Return True if broker is not soft-deleted."""
        return not self.broker.is_deleted

    # ---------------------------------------------------------
    # DEBUG
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"Broker(company={self.broker.company_name}, id={self.broker.id})"
