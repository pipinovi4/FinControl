from locales import register

from .titles import TITLES
from .buttons import BUTTONS
from .ui import UI
from .bodies import BODIES
from .steps import STEPS
from .steps_by_country import STEPS_BY_COUNTRY
from .common import COMMON

L10N_RU = {
    "titles": TITLES,
    "buttons": BUTTONS,
    "ui": UI,
    "bodies": BODIES,
    "steps": STEPS,
    "steps_by_country": STEPS_BY_COUNTRY,
    "common": COMMON,
}

register("ru", L10N_RU)

__all__ = ["L10N_RU"]
