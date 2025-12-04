STEPS_BY_COUNTRY = {
    "RU": {
        "id_number": {
            "label": "Идентификатор",
            "prompt": "🆔 СНИЛС (XXX-XXX-XXX YY).",
            "quick": None,
        },
        "inn_ru": {
            "label": "ИНН",
            "prompt": "🔢 Укажите ваш ИНН (10 или 12 цифр).",
            "quick": None,
        },
    },

    "BY": {
        "id_number": {
            "label": "Идентификатор",
            "prompt": "🆔 Ваш личный номер (паспортный ID).",
            "quick": None,
        },
    },

    "KZ": {
        "id_number": {
            "label": "Идентификатор",
            "prompt": "🆔 ИИН (ЖСН).",
            "quick": None,
        },
    },
}

__all__ = ["STEPS_BY_COUNTRY"]
