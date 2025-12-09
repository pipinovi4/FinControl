# routes/entities/analyze/types.py
from typing import Tuple, Type, TypeVar
from enum import Enum

from app.utils.protocols import BaseService
from app.schemas.entities.filters import (
    WorkerFilterSchema, BrokerFilterSchema,
    AdminFilterSchema, UserFilterSchema
)

# ⛔ NOTICE:
# ClientFilterSchema видаляється з системи разом із Legacy Client
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


class AnalyzeType(str, Enum):
    """
    Supported analytics metrics.

    Each value must correspond to a method named `run_<metric>`
    inside the appropriate Service class.
    """

    # ─────────────────────────────────────────────
    # 📂 Application-centric metrics (MAIN FOCUS)
    # ─────────────────────────────────────────────

    APPLICATIONS_GROWTH = "applications_growth"              # Trend of created applications over time
    APPLICATIONS_PER_BROKER = "applications_per_broker"      # Distribution of applications by broker
    APPLICATIONS_PER_WORKER = "applications_per_worker"      # Distribution of applications by worker

    APPLICATIONS_SUMMARY = "applications_summary"            # Total, approved, rejected, pending
    APPLICATIONS_OVER_TIME = "applications_over_time"        # Apps per day/week/month
    APPLICATIONS_BY_SOURCE = "applications_by_source"        # Source channels segmentation

    # ─────────────────────────────────────────────
    # 💰 Financial metrics
    # ─────────────────────────────────────────────
    REVENUE_PER_DAY = "revenue_per_day"                      # Issued credits per day
    AVERAGE_AMOUNT = "average_amount"                        # Avg issued amount
    TOTAL_REVENUE = "total_revenue"                          # Sum(amount) of all credit operations

    # ─────────────────────────────────────────────
    # 👥 User activity metrics
    # ─────────────────────────────────────────────
    ACTIVE_USERS_TODAY = "active_users_today"
    LAST_LOGIN_DISTRIBUTION = "last_login_distribution"

    # ─────────────────────────────────────────────
    # 🏢 Organizational metrics
    # ─────────────────────────────────────────────
    BROKERS_ACTIVITY = "brokers_activity"                    # Activity level based on app count
    WORKERS_ACTIVITY = "workers_activity"                    # Same but for workers

    # ─────────────────────────────────────────────
    # 📊 System diagnostics
    # ─────────────────────────────────────────────
    SYSTEM_LOAD = "system_load"
    ERRORS_PER_DAY = "errors_per_day"
