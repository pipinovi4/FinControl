from backend.app.models.entities import Broker
from typing import Optional


class BrokerUtils:
    """
    Utility class for handling Broker-related logic.

    Contains static helper methods to simplify checks and validations
    (e.g. region matching, role checks).
    """

    @staticmethod
    def is_region_match(broker: Broker, region: str) -> bool:
        """
        Check if the broker operates in a specific region.

        :param broker: Broker instance
        :param region: Region to check (case-insensitive)
        :return: True if region is in broker's list
        """
        return any(r.lower() == region.lower() for r in broker.region or [])

    @staticmethod
    def get_main_region(broker: Broker) -> Optional[str]:
        """
        Return the first region the broker is assigned to (if any).

        :param broker: Broker instance
        :return: The main region or None
        """
        return broker.region[0] if broker.region else None

    @staticmethod
    def get_clients_count(broker: Broker) -> int:
        """
        Return number of clients assigned to the broker.

        :param broker: Broker instance
        :return: Integer count of clients
        """
        return len(broker.clients or [])

    @staticmethod
    def has_clients(broker: Broker) -> bool:
        """
        Check whether the broker has any assigned clients.

        :param broker: Broker instance
        :return: True if at least one client is assigned
        """
        return bool(broker.clients)

    @staticmethod
    def get_company_display(broker: Broker) -> str:
        """
        Get the display name for the broker's company.

        :param broker: Broker instance
        :return: Company name or fallback
        """
        return broker.company_name or f"Broker#{str(broker.id)[:6]}"
