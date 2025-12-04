from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from locales import L10N, translate as t


def build_keyboard(lang: str, country: str, step_key: str):
    locale = L10N.get(lang, {})
    steps = locale.get("steps", {})
    steps_by_country = locale.get("steps_by_country", {})
    quick_map = locale.get("quick", {})

    # --------------------------
    # Correct country override
    # --------------------------
    cfg = steps_by_country.get(country, {}).get(step_key)
    if not cfg:
        cfg = steps.get(step_key, {})

    # ============================================================
    # 1. DIRECT PHONE INPUT
    # ============================================================
    if cfg.get("input") == "phone":
        return ReplyKeyboardMarkup(
            [
                [KeyboardButton(t(lang, "steps.share_phone"), request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    # ============================================================
    # 2. STATIC OPTIONS
    # ============================================================
    options = cfg.get("options")
    if isinstance(options, list) and options:
        return ReplyKeyboardMarkup(
            [[KeyboardButton(o)] for o in options],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    # ============================================================
    # 3. QUICK BUTTONS
    # ============================================================
    quick_opts = cfg.get("quick")
    if isinstance(quick_opts, list) and quick_opts:
        rows = []

        for item in quick_opts:

            # contact button
            if isinstance(item, dict) and item.get("type") == "contact":
                rows.append([KeyboardButton(
                    text=item.get("text", "📱 Отправить номер"),
                    request_contact=True
                )])
                continue

            # canonical buttons
            if isinstance(item, dict) and "text" in item:
                rows.append([KeyboardButton(item["text"])])
                continue

            # plain string button
            rows.append([KeyboardButton(str(item))])

        return ReplyKeyboardMarkup(
            rows,
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    # ============================================================
    # 4. YES / NO
    # ============================================================
    if cfg.get("input") == "yesno":
        yes, no = quick_map.get("yes_no", ["Yes", "No"])

        return ReplyKeyboardMarkup(
            [
                [KeyboardButton(yes)],
                [KeyboardButton(no)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

    # ============================================================
    # 5. DEFAULT
    # ============================================================
    return ReplyKeyboardRemove()

__all__ = [
    "build_keyboard",
]