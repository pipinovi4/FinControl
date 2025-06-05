from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime, UTC

class TimeStampAuthMixin:
    """
    Adds a timestamp for tracking the last login time.
    """
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
