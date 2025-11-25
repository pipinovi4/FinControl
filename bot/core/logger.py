# core/logger.py
import logging

# Unified logging format used across the entire bot.
# This ensures every module prints logs in the same readable structure:
#   2025-01-01 12:00:00 INFO [module] message
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def setup_logging(level=logging.INFO):
    """
    Initializes the global logging configuration.

    This function should be called exactly once during application startup
    (typically from main.py) to apply a consistent logging format and level.

    Parameters
    ----------
    level : int
        Logging verbosity level, e.g. logging.INFO or logging.DEBUG.
    """
    logging.basicConfig(
        format=LOG_FORMAT,
        level=level,
    )


# Global logger instance.
# Any module can import `log` instead of creating its own logger.
# Example:
#     from core.logger import log
#     log.info("Something happened")
log = logging.getLogger("worldflow")


__all__ = ["log", "setup_logging"]
