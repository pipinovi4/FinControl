"""
Schema mixins package initializer.

This module exposes reusable Pydantic schema mixins that encapsulate common fields and logic.
These mixins are meant to be inherited by other schemas to avoid repetition and ensure consistency.
"""

from .Auth import AuthSchema                  # Adds email and password hash fields for authentication
from .DynamicLinkAuth import DynamicLinkAuthSchema  # Adds dynamic link authentication support
from .TelegramBase import TelegramBaseSchema  # Adds Telegram ID field and basic Telegram user info
from .TimeStamp import TimeStampSchema        # Adds created_at and updated_at fields
from .TimeStampAuth import TimeStampAuthSchema  # Extends TimeStamp with last_login tracking
from .UUID import UUIDSchema                  # Adds UUID primary key field
from .SoftDeleteSchema import SoftDeleteSchema  # Adds is_deleted flag for soft delete behavior

# Public API of the schema mixins package
__all__ = [
    "AuthSchema",
    "UUIDSchema",
    "TimeStampSchema",
    "TelegramBaseSchema",
    "TimeStampAuthSchema",
    "DynamicLinkAuthSchema",
    "SoftDeleteSchema",
]
