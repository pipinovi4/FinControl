def resolve_canonical(step_cfg, user_value: str):
    """
    Returns:
        {
            "canonical": "...",   # for branching
            "display":   "..."    # for UI
        }
    """

    quick = step_cfg.get("quick")

    # Free text input — no quick options here
    if not isinstance(quick, list):
        return {
            "canonical": user_value,
            "display": user_value,
        }

    for item in quick:

        # new format: {"key": "Employed", "text": "Наёмный сотрудник"}
        if isinstance(item, dict) and "key" in item and "text" in item:
            if item["text"] == user_value:
                return {
                    "canonical": item["key"],
                    "display": item["text"],
                }

        # old format: ["Employed", "Self-employed", ...]
        if isinstance(item, str) and item == user_value:
            return {
                "canonical": item,
                "display": item,
            }

    # Nothing matched — treat raw value as-is
    return {
        "canonical": user_value,
        "display": user_value,
    }

__all__ = ["resolve_canonical"]