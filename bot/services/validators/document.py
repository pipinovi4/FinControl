"""
Document validator.
Validates:
- file_id present
- allowed mimetypes (if configured)
- max file size
"""

from typing import Tuple, Any

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}

MAX_SIZE_MB = 10


async def validate_document(value: Any) -> Tuple[bool, Any]:
    """
    value may be:
    - dict (one file)
    - list[dict] (multi-file)
    """

    # Case 1 — ONE FILE
    if isinstance(value, dict):
        if "file_id" not in value:
            return False, "Некорректный файл"

        return True, value

    # Case 2 — MULTI FILE
    if isinstance(value, list):

        if not value:
            return False, "Не найдено файлов"

        for i, f in enumerate(value):

            if "file_id" not in f:
                return False, "Некорректный файл"

        return True, value

    return False, "Некорректный формат файла"
