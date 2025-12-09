# routes/entities/analyze/types.py
from typing import Tuple, Type, TypeVar
from enum import Enum

from app.utils.protocols import BaseService
from app.schemas.entities.filters import (
    WorkerFilterSchema, BrokerFilterSchema,
    AdminFilterSchema, UserFilterSchema
)

# ⛔ NOTICE:
FilterSchemaT = TypeVar(
    "FilterSchemaT",
    AdminFilterSchema,
    WorkerFilterSchema,
    BrokerFilterSchema,
    UserFilterSchema,
)

RawTuple = Tuple[
    str,
    Type[BaseService],  # worker service
    Type[BaseService],  # broker service
    Type[BaseService],  # admin service
    Type[FilterSchemaT]
]


from enum import Enum

class AnalyzeType(str, Enum):
    """
    Application-centric analytics metrics.
    """

    # Applications
    APPLICATIONS_GROWTH = "applications_growth"
    APPLICATIONS_PER_BROKER = "applications_per_broker"
    APPLICATIONS_PER_WORKER = "applications_per_worker"

    APPLICATIONS_SUMMARY = "applications_summary"
    APPLICATIONS_OVER_TIME = "applications_over_time"
    APPLICATIONS_BY_SOURCE = "applications_by_source"

    # Financial
    REVENUE_PER_DAY = "revenue_per_day"
    AVERAGE_AMOUNT = "average_amount"
    TOTAL_REVENUE = "total_revenue"

    # User-related
    ACTIVE_USERS_TODAY = "active_users_today"
    LAST_LOGIN_DISTRIBUTION = "last_login_distribution"

    # Organization
    BROKERS_ACTIVITY = "brokers_activity"
    WORKERS_ACTIVITY = "workers_activity"

    # System
    SYSTEM_LOAD = "system_load"
    ERRORS_PER_DAY = "errors_per_day"
