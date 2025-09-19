from datetime import datetime

class TimeStampAuthSchema:
    """
    Shared schema for exposing the last login timestamp of a user.
    Used in Out schemas for role-based models (e.g., Worker, Broker).
    """

    last_login_at: datetime | None = None  # Nullable — користувач міг ще не логінитись

