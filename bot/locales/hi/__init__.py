from locales import register

from .titles import TITLES
from .buttons import BUTTONS
from .ui import UI
from .bodies import BODIES
from .labels import LABELS
from .steps import STEPS
from .steps_by_country import STEPS_BY_COUNTRY
from .quick import QUICK

L10N_HI = {
    "titles": TITLES,
    "buttons": BUTTONS,
    "ui": UI,
    "bodies": BODIES,
    "steps": STEPS,
    "labels": LABELS,
    "steps_by_country": STEPS_BY_COUNTRY,
    "quick": QUICK,
}

register("hi", L10N_HI)

__all__ = ["L10N_HI"]
