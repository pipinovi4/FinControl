"""
Date range validator.

Expected format:
    DD.MM.YYYY - DD.MM.YYYY

Checks:
    • correct format of both dates
    • start <= end
    • year range reasonable (1900–2100)
"""

import re
from datetime import datetime
from typing import Tuple
from .base import ok, error


DATE_RE = re.compile(
    r"^\s*(\d{2}\.\d{2}\.\d{4})\s*[-–]\s*(\d{2}\.\d{2}\.\d{4})\s*$"
)


async def validate_date_range(value: str) -> Tuple[bool, str]:
    m = DATE_RE.match(value)
    if not m:
        return error("Введите даты в формате: ДД.ММ.ГГГГ - ДД.ММ.ГГГГ")

    start_s, end_s = m.groups()

    try:
        start = datetime.strptime(start_s, "%d.%m.%Y")
        end = datetime.strptime(end_s, "%d.%m.%Y")
    except ValueError:
        return error("Некорректная дата. Проверьте правильность ввода.")

    if start.year < 1900 or end.year > 2100:
        return error("Год должен быть в диапазоне 1900–2100.")

    if start > end:
        return error("Дата начала не может быть позже даты окончания.")

    return ok()


__all__ = ["validate_date_range"]
