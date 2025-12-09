from typing import Type, TypeVar, List
from app.models import Worker
from app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)


class ApplicationWorkerUtilService:
    """
    Utility service for performing lightweight, stateless transformations
    related to Worker → Application relationships.

    This service is meant for quick in-memory operations such as:

        - Filtering workers by number of assigned applications
        - Converting ORM objects to Pydantic schemas
        - Preparing lightweight DTOs for display layers

    It does NOT perform any DB calls and is safe to use in synchronous code.

    Methods:
        - filter_by_applications_count(workers, min_apps)
        - to_schema(workers, schema)
        - to_schema_one(worker, schema)
        - get_display_name(worker)

    Intended use:
        workers = service.filter_by_applications_count(list_of_workers, 2)
        payload = service.to_schema(workers, WorkerSchema.Out)
    """

    # ----------------------------------------------------------
    # FILTERING
    # ----------------------------------------------------------
    @staticmethod
    def filter_by_applications_count(
        workers: List[Worker],
        min_apps: int
    ) -> List[Worker]:
        """
        Return only workers who have at least `min_apps` assigned applications.
        """
        return [
            w for w in workers
            if w.applications and len(w.applications) >= min_apps
        ]

    # ----------------------------------------------------------
    # SCHEMA CONVERSION
    # ----------------------------------------------------------
    @staticmethod
    def to_schema(workers: List[Worker], schema: Type[T]) -> List[T]:
        """
        Convert a list of Workers to Pydantic schema objects.
        """
        if not hasattr(schema, "model_validate"):
            raise TypeError("Schema class must implement model_validate()")

        return [schema.model_validate(worker) for worker in workers]

    @staticmethod
    def to_schema_one(worker: Worker, schema: Type[T]) -> T:
        """
        Convert a single Worker to schema.
        """
        if not hasattr(schema, "model_validate"):
            raise TypeError("Schema class must implement model_validate()")

        return schema.model_validate(worker)

    # ----------------------------------------------------------
    # DISPLAY HELPERS
    # ----------------------------------------------------------
    @staticmethod
    def get_display_name(worker: Worker) -> str:
        """
        Returns readable display name for UI:
        - worker.username if exists
        - or fallback "Worker#xxxxxx"
        """
        if worker.username:
            return worker.username

        return f"Worker#{str(worker.id)[:6]}"
