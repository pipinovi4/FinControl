from typing import Type, TypeVar
from backend.app.models import Client
from backend.app.schemas import SchemaBase
from backend.app.services.entities import UserUtilService

T = TypeVar("T", bound=SchemaBase)


class ClientUtilService(UserUtilService):
    """
    Utility functions for working with client-related data.
    All methods are static and operate on raw inputs or lists of clients.
    """

    @staticmethod
    def get_display_name(client: Client) -> str:
        """
        Return a display-friendly name for a client.

        Prefer full_name, fallback to telegram username or UUID.

        :param client: A Client instance.
        :return: Display name string.
        """
        if client.full_name:
            return client.full_name
        return f"Client#{str(client.id)[:6]}"

    @staticmethod
    def filter_by_worker(clients: list[Client], worker_id: str) -> list[Client]:
        """
        Filter clients assigned to a specific worker.

        :param clients: List of Client instances.
        :param worker_id: UUID string of the worker.
        :return: Filtered list of clients.
        """
        return [client for client in clients if str(client.worker_id) == worker_id]

    @staticmethod
    def filter_verified(clients: list[Client]) -> list[Client]:
        """
        Filter clients who have provided income proof and report files.

        :param clients: List of Client instances.
        :return: List of verified clients.
        """
        return [client for client in clients if client.income_proof and client.report_files]

    @staticmethod
    def to_schema(clients: list[Client], schema: Type[T]) -> list[T]:
        """
        Convert a list of Client ORM instances to a list of Pydantic schemas.

        :param clients: List of Client instances.
        :param schema: A Pydantic schema class that supports `model_validate`.
        :return: List of schema representations.

        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")

        return [schema.model_validate(client) for client in clients]

    @staticmethod
    def to_schema_one(client: Client, schema: Type[T]) -> T:
        """
        Convert a single Client ORM instance to a Pydantic schema instance.

        :param client: A single Client instance (SQLAlchemy model).
        :param schema: A Pydantic schema class that supports `model_validate`.
        :return: A schema instance representing the client.

        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")

        return schema.model_validate(client)