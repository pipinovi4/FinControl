# backend/app/services/entities/application/application_filter.py
from sqlalchemy import select
from sqlalchemy.sql import Select

from app.models.entities.application import Application


class ApplicationFilterService:
    """Fluent SQL builder for filtering Applications."""

    def __init__(self):
        self.query: Select = select(Application)

    def by_worker(self, worker_id):
        self.query = self.query.where(Application.worker_id == worker_id)
        return self

    def by_broker(self, broker_id):
        self.query = self.query.where(Application.broker_id == broker_id)
        return self

    def only_active(self):
        self.query = self.query.where(Application.is_deleted == False)
        return self

    def by_telegram(self, telegram_id):
        self.query = self.query.where(Application.telegram_id == telegram_id)
        return self

    def apply(self) -> Select:
        return self.query
