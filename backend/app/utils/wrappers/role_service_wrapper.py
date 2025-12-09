from __future__ import annotations

import inspect
import logging
from typing import Any, Generic, TypeVar, Union, Set

from app.utils.protocols import BaseService

S = TypeVar("S", bound=BaseService)


class RoleServiceWrapper(Generic[S]):
    """
    Runtime-proxy that lets you expose **only** methods defined directly
    on the given service class (i.e., no inherited 'super-admin' helpers).

    This version does NOT create an instance until `.get_instance(db)` is called.

    Parameters
    ----------
    svc_or_cls : type[S]
        A service class (`AdminService`, `ApplicationService`, etc).
    extra_allowed : Optional set of additional method names to expose.
    """

    __slots__ = ("_klass", "_whitelist")

    def __init__(
        self,
        svc_or_cls: type[S],
        *,
        extra_allowed: Set[str] | None = None,
    ) -> None:
        klass = self._normalize(svc_or_cls)

        whitelist = self._own_methods(klass)
        if extra_allowed:
            whitelist.update(extra_allowed)

        self._klass: type[S] = klass
        self._whitelist: Set[str] = whitelist

    def get_instance(self, db) -> S:
        """Create a new service instance with a given DB session."""
        return self._klass(db)

    def allowed(self) -> Set[str]:
        """Return a *copy* of the current whitelist."""
        return set(self._whitelist)

    def __dir__(self) -> list[str]:
        return sorted(self._whitelist)

    def __getattr__(self, name: str) -> Any:
        raise RuntimeError(
            f"Direct access to methods is blocked for security. "
            f"Use `.get_instance(db).{name}(...)` instead."
        )

    def __repr__(self) -> str:
        cls_name = self._klass.__name__
        return f"<RoleServiceWrapper[{cls_name}] allowed={sorted(self._whitelist)}>"

    @staticmethod
    def _normalize(obj: type[S]) -> type[S]:
        if not inspect.isclass(obj):
            raise TypeError(f"Expected class, got instance: {obj}")
        return obj

    @staticmethod
    def _own_methods(klass: type[S]) -> Set[str]:
        return {
            name
            for name, val in klass.__dict__.items()
            if callable(val) and not name.startswith("__")
        }
