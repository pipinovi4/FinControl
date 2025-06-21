# routes/entities/analyze/types.py
from typing import Tuple, Type, TypeVar
from enum import Enum

from backend.app.utils.protocols import BaseService
from backend.app.schemas.entities.filters import (
    WorkerFilterSchema, BrokerFilterSchema, ClientFilterSchema, AdminFilterSchema, UserFilterSchema
)

FilterSchemaT = TypeVar("FilterSchemaT", AdminFilterSchema, ClientFilterSchema, WorkerFilterSchema, BrokerFilterSchema, UserFilterSchema)

RawTuple = Tuple[
    str,
    Type[BaseService], Type[BaseService],
    Type[BaseService], Type[FilterSchemaT],
]

class AnalyzeType(str, Enum):
    """
    Supported analytics metrics.

    Each value must correspond to a method named `run_<metric>`
    in the appropriate Service class. Example: `run_clients_growth`.
    """

    # 📈 Clients
    CLIENTS_GROWTH = "clients_growth"                    # Client registration trend over time
    CLIENTS_PER_BROKER = "clients_per_broker"            # Distribution of clients by broker
    CLIENTS_PER_WORKER = "clients_per_worker"            # Distribution of clients by worker

    # 🗂 Applications
    APPLICATIONS_SUMMARY = "applications_summary"        # Total, approved, rejected stats
    APPLICATIONS_OVER_TIME = "applications_over_time"    # Number of applications per day/week
    APPLICATIONS_BY_SOURCE = "applications_by_source"    # Applications segmented by source/channel

    # 💸 Financial
    REVENUE_PER_DAY = "revenue_per_day"                  # Revenue trends per day
    AVERAGE_AMOUNT = "average_amount"                    # Average amount per application
    TOTAL_REVENUE = "total_revenue"                      # Total issued funds across all clients

    # 👤 User activity
    ACTIVE_USERS_TODAY = "active_users_today"            # Number of users active today
    LAST_LOGIN_DISTRIBUTION = "last_login_distribution"  # How recently users have logged in

    # 🏢 Organization
    BROKERS_ACTIVITY = "brokers_activity"                # Applications handled per broker
    WORKERS_ACTIVITY = "workers_activity"                # Applications handled per worker

    # 📊 System diagnostics
    SYSTEM_LOAD = "system_load"                          # Number of DB entities or heavy resources
    ERRORS_PER_DAY = "errors_per_day"                    # System errors grouped by day
