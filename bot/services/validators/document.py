"""
Document validator.
Validates:
- file_id present
- allowed mimetypes (if configured)
- max file size
"""

from typing import Tuple
from .base import ok, error

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}

MAX_SIZE_MB = 10


async def validate_document(value: dict) -> Tuple[bool, str]:
    """
    value = {
        "file_id": str,
        "mime": str,
        "size": int,
        "name": str
    }
    """

    if not isinstance(value, dict):
        return error("errors.invalid_file")

    file_id = value.get("file_id")
    mime = value.get("mime")
    size = value.get("size", 0)

    if not file_id:
        return error("errors.no_document")

    if mime and mime not in ALLOWED_TYPES:
        return error("errors.unsupported_file_type")

    if size > MAX_SIZE_MB * 1024 * 1024:
        return error("errors.file_too_large")

    return ok()
