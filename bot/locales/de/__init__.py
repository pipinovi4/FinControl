from locales import register

from .titles import TITLES
from .buttons import BUTTONS
from .ui import UI
from .bodies import BODIES
from .steps import STEPS
from .labels import LABELS
from .steps_by_country import STEPS_BY_COUNTRY

L10N_DE = {
    "titles": TITLES,
    "buttons": BUTTONS,
    "ui": UI,
    "bodies": BODIES,
    "steps": STEPS,
    "labels": LABELS,
    "steps_by_country": STEPS_BY_COUNTRY,
}

register("de", L10N_DE)

__all__ = ["L10N_DE"]
