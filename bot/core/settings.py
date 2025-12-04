from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional

import logging

log = logging.getLogger("settings")


class SettingsError(Exception):
    """Raised when environment configuration is invalid."""
    pass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    support_username: str
    app_name: str


def _read_env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key, default)
    if value is None or value == "":
        raise SettingsError(f"Environment variable '{key}' is required but missing.")
    return value


def load_settings(debug: bool = False) -> Settings:
    """
    Loads environment variables with strict validation.
    Logs values (masked) if debug=True.
    """

    try:
        bot_token = _read_env("TELEGRAM_BOT_TOKEN")
        support_username = _read_env("SUPPORT_USERNAME", "WorldFlowSupport")
        app_name = _read_env("APPLICATION_NAME", "WorldFlow Credit")

        if debug:
            log.warning("=== Settings Debug ===")
            log.warning("TELEGRAM_BOT_TOKEN = %s***", bot_token[:8])
            log.warning("SUPPORT_USERNAME = %s", support_username)
            log.warning("APPLICATION_NAME = %s", app_name)

        return Settings(
            bot_token=bot_token,
            support_username=support_username,
            app_name=app_name
        )

    except SettingsError as e:
        log.error("❌ Settings error: %s", e)
        raise

    except Exception as e:
        log.exception("Unexpected error while loading settings")
        raise
