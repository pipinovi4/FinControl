from app.models import Client
from app.services.entities import UserInterfaceService


class ClientInterfaceService(UserInterfaceService):
    """
    Interface class for accessing and interpreting client-related state and properties.

    Extends UserInterfaceService, adding client-specific logic such as
    worker assignment and verification status.
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize the interface with a Client instance.

        :param client: The Client model instance.
        """
        super().__init__(client)
        self.client = client

    def has_assigned_worker(self) -> bool:
        """
        Check if the client has an assigned worker.

        A client is considered assigned if `worker_id` is not None.

        :return: True if a worker is assigned, False otherwise.
        """
        return self.client.worker_id is not None

    def is_verified(self) -> bool:
        """
        Check if the client has completed all required verifications.

        A client is considered verified if both income_proof and report_files are provided.

        :return: True if both fields are non-empty, False otherwise.
        """
        return bool(self.client.income_proof and self.client.report_files)
