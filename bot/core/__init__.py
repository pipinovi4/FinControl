# Package initializer for the bot's core public API.
#
# This file re-exports the most important configuration objects,
# constants, and logging utilities, allowing other modules to import them
# cleanly from `bot` instead of referencing deep internal paths.
#
# Example:
#     from bot import load_settings, log
#
# This keeps the import structure clean and stable, even if internal folders change.

from .settings import (
    COUNTRIES_BY_REGION,
    REGIONS,
    load_settings,
    LANG_BY_COUNTRY,
    COUNTRY_TITLE,
)

from .logger import setup_logging, log


# Define the public API surface.
# Only the names listed here will be imported when someone uses:
#     from bot import *
#
# This also serves as documentation for which parts of the package are considered stable.
__all__ = [
    "load_settings",
    "REGIONS",
    "COUNTRIES_BY_REGION",
    "LANG_BY_COUNTRY",
    "COUNTRY_TITLE",
    "setup_logging",
    "log",
]
