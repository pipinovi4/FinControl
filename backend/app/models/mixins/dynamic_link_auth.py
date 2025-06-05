from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class DynamicLinkAuthMixin:
    """
    Mixin for authentication via dynamic login links.
    """
    dynamic_login_token: Mapped[str] = mapped_column(String(64), nullable=True)
