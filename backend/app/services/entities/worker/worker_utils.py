from typing import Type, TypeVar, List
from app.models import Worker
from app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)

class WorkerUtilService:
    """
    Static utility service for transforming and filtering Worker model data.

    This service is designed for lightweight, stateless manipulation of Worker entities,
    including formatting display names, filtering based on client assignments,
    and converting ORM objects to Pydantic schemas.

    Intended Use-Cases:
        - Preparing data for frontend views or API responses.
        - Lightweight transformation pipelines outside of main service logic.
        - DRY utility layer for schema conversion or display name formatting.

    Methods:
        - filter_by_clients_count(workers, min_clients): Filters workers by client count.
        - to_schema(workers, schema): Converts list of Workers to schema objects.
        - to_schema_one(worker, schema): Converts a single Worker to schema object.

    Example:
        workers = get_some_workers()
        filtered = WorkerUtilService.filter_by_clients_count(workers, min_clients=3)
        schemas = WorkerUtilService.to_schema(filtered, WorkerSchema.Out)
        display = WorkerUtilService.get_display_name(filtered[0])
    """

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