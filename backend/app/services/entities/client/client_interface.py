from backend.app.models import Client
from backend.app.services.entities import UserInterfaceService


class ClientInterfaceService(UserInterfaceService):
    """
    Interface class for accessing and interpreting client-related state and properties.

    Extends UserInterfaceService, adding client-specific logic.
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize the interface with a Client instance.

        :param client: The Client model instance.
        """
        super().__init__(client)
        self.client = client

    def has_assigned_worker(self) -> bool:
        """Check if the client has an assigned worker."""
        return self.client.worker_id is not None

    def is_verified(self) -> bool:
        """Check if the client has completed all required verifications."""
        return bool(self.client.income_proof and self.client.report_files)