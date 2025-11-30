from locales import register

from .titles import TITLES
from .buttons import BUTTONS
from .ui import UI
from .bodies import BODIES
from .labels import LABELS
from .steps import STEPS
from .steps_by_country import STEPS_BY_COUNTRY


L10N_EN = {
    "titles": TITLES,
    "buttons": BUTTONS,
    "ui": UI,
    "bodies": BODIES,
    "labels": LABELS,
    "steps": STEPS,
    "steps_by_country": STEPS_BY_COUNTRY,
}

register("en", L10N_EN)

__all__ = ["L10N_EN"]
