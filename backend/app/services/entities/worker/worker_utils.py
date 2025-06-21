from typing import Type, TypeVar, List
from backend.app.models import Worker
from backend.app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)

class WorkerUtilService:
    """
    Utility functions for working with worker-related data.
    All methods are static and operate on raw Worker instances or lists of workers.
    """

    @staticmethod
    def get_display_name(worker: Worker) -> str:
        """
        Return a display-friendly name for a worker.
        Prefer Telegram username if available, otherwise use the system username.
        :param worker: A Worker instance.
        :return: Display name string.
        """
        if worker.telegram_username:
            return f"@{worker.telegram_username}"
        return worker.username

    @staticmethod
    def filter_by_clients_count(workers: List[Worker], min_clients: int) -> List[Worker]:
        """
        Filter the list of workers to include only those with at least min_clients assigned.
        :param workers: List of Worker instances.
        :param min_clients: Minimum number of assigned clients.
        :return: Filtered list of workers.
        """
        return [worker for worker in workers if worker.clients and len(worker.clients) >= min_clients]

    @staticmethod
    def to_schema(workers: List[Worker], schema: Type[T]) -> List[T]:
        """
        Convert a list of Worker ORM instances to a list of Pydantic schema instances.
        :param workers: List of Worker instances.
        :param schema: A Pydantic schema class that supports 'model_validate'.
        :return: List of schema instances representing the workers.
        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")
        return [schema.model_validate(worker) for worker in workers]

    @staticmethod
    def to_schema_one(worker: Worker, schema: Type[T]) -> T:
        """
        Convert a single Worker ORM instance to a Pydantic schema instance.
        :param worker: A single Worker instance.
        :param schema: A Pydantic schema class that supports 'model_validate'.
        :return: A schema instance representing the worker.
        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")
        return schema.model_validate(worker)