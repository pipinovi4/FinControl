# backend/app/utils/decorators/db_errors.py
import asyncio
import logging
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

from fastapi import HTTPException, status
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

T = TypeVar("T", bound=Callable[..., Any])
logger = logging.getLogger(__name__)


def handle_exceptions(
    *,
    default_return: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    raise_404: bool = False,
) -> Callable[[T], T]:
    """
    Декоратор-«зонт» для будь-яких методів, що працюють із БД (sync / async).

    • ловить IntegrityError і мапить найбільш поширені pg-коди
      - 23505 → 409 «Объект с такими данными уже существует»
      - 23503 → 400 «Нарушение внешнего ключа»
      - иное  → 422 «Нарушение ограничений целостности данных»

    • автоматично виконує ROLLBACK, якщо у `self` є `db`

    • за `raise_404=True` піднімає 404, коли результат `None`

    • будь-які інші SQLAlchemyError → 500 (або `default_status`)
    """

    def decorator(func: T) -> T:  # type: ignore[misc]
        async def _async(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if raise_404 and result is None:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Не найдено")
                return result
            except IntegrityError as exc:
                await _rollback(args)
                _raise_integrity(exc)
            except SQLAlchemyError as exc:
                await _rollback(args)
                logger.exception("SQLAlchemy error in %s", func.__name__, exc)
                raise HTTPException(default_return, "Ошибка базы данных") from exc

        def _sync(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if raise_404 and result is None:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Не найдено")
                return result
            except IntegrityError as exc:
                _rollback(args, sync=True)
                _raise_integrity(exc)
            except SQLAlchemyError as exc:
                _rollback(args, sync=True)
                logger.exception("SQLAlchemy error in %s", func.__name__, exc)
                raise HTTPException(default_return, "Ошибка базы данных") from exc

        @wraps(func)
        def wrapper(*args, **kwargs):  # type: ignore[override]
            return _async(*args, **kwargs) if asyncio.iscoroutinefunction(func) else _sync(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


# ───────────────────── helpers ─────────────────────
async def _rollback(args, *, sync: bool = False):
    """Пробуем сделать rollback, если у self есть .db"""
    db = getattr(args[0], "db", None)
    if not db:
        return
    try:
        if sync:
            db.rollback()
        else:
            await db.rollback()
    except Exception:  # noqa: BLE001
        pass


def _raise_integrity(exc: IntegrityError) -> None:  # pragma: no cover
    """Бросает HTTPException с корректным статусом и сообщением."""
    pgcode = getattr(exc.orig, "pgcode", None)

    if pgcode == errorcodes.UNIQUE_VIOLATION:  # 23505
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Объект с такими данными уже существует",
        ) from exc

    if pgcode == errorcodes.FOREIGN_KEY_VIOLATION:  # 23503
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Нарушение внешнего ключа",
        ) from exc

    raise HTTPException(  # прочие IntegrityError
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Нарушение ограничений целостности данных",
    ) from exc
