from __future__ import annotations
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

# === Base application settings ===
# This dataclass stores all core environment-driven configuration
# values required by the bot. It ensures strict typing and immutability.
@dataclass(frozen=True)
class Settings:
    bot_token: str
    support_username: str
    app_name: str


def load_settings() -> Settings:
    """
    Loads all required environment variables for the bot.
    Raises an explicit error if a critical variable is missing.
    This function is executed once during application bootstrap.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    support_username = os.getenv("SUPPORT_USERNAME", "WorldFlowSupport")
    app_name = os.getenv("APPLICATION_NAME", "WorldFlow Credit")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Put it in environment or .env")

    if not support_username:
        raise RuntimeError("SUPPORT_USERNAME is not set. Put it in environment or .env")

    return Settings(
        bot_token=token,
        support_username=support_username,
        app_name=app_name,
    )

# Export only what should be visible outside this module
__all__ = ["load_settings"]
