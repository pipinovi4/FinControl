from typing import TypeVar

from app.models import Broker
from app.services.entities import UserInterfaceService

BrokerT = TypeVar("BrokerT", bound=Broker)


class BrokerInterfaceService(UserInterfaceService):
    """
    BrokerInterfaceService — wrapper around the Broker model.

    Provides helper methods to access broker-specific attributes,
    simplify view rendering, and encapsulate common logic.

    TypeVars:
        BrokerT — any entity subclassing Broker.

    Includes:
        - get_display_name(): Display broker's company or fallback.
        - get_email(): Return broker's email.
        - get_regions(): List of broker's active regions.
        - get_clients_count(): Return number of assigned clients.
        - has_clients(): Check if broker has any clients.
        - is_active(): Check if broker is active (not soft-deleted).
        - __str__(): Developer-friendly string for debugging.
    """
    def __init__(self, broker: BrokerT):
        super().__init__(broker)
        self.broker: BrokerT = broker

    def get_display_name(self) -> str:
        """Return broker’s company name or fallback."""
        return self.broker.company_name or f"Broker#{str(self.broker.id)[:6]}"

    def get_email(self) -> str:
        """Return broker’s email."""
        return str(self.broker.email)

    def get_regions(self) -> list[str]:
        """Return list of broker’s regions."""
        return self.broker.region or []

    def get_clients_count(self) -> int:
        """Return the number of clients assigned to the broker."""
        return len(self.broker.clients or [])

    def has_clients(self) -> bool:
        """Return True if the broker has at least one client."""
        return bool(self.broker.clients)

    def is_active(self) -> bool:
        """Return True if broker is not soft-deleted."""
        return not self.broker.is_deleted

    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Broker(company={self.broker.company_name}, id={self.broker.id})"
