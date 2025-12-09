# backend/app/services/entities/application/application_utils.py
from typing import Type, TypeVar, List

from app.models.entities.application import Application
from app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)


class ApplicationUtilService:

    @staticmethod
    def extract_display_name(app: Application) -> str:
        d = app.data
        return d.get("full_name") or f"Application#{str(app.id)[:6]}"

    @staticmethod
    def to_schema_list(applications: List[Application], schema: Type[T]) -> List[T]:
        return [schema.model_validate(a) for a in applications]

    @staticmethod
    def to_schema_one(app: Application, schema: Type[T]) -> T:
        return schema.model_validate(app)
