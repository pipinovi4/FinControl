from __future__ import annotations

import inspect
import logging
from typing import Any, Generic, TypeVar, Union, Set

from backend.app.utils.protocols import BaseService

S = TypeVar("S", bound=BaseService)

class RoleServiceWrapper(Generic[S]):
    """
    Runtime-proxy that lets you expose **only** methods defined directly
    on the given service class (i.e., no inherited 'super-admin' helpers).

    Parameters
    ----------
    svc_or_cls : Union[type[S], S]
        A service class (`AdminService`) *or* an already created instance.
    extra_allowed : Set[str] | None
        Optional set of additional method names to expose (rarely needed).
    """

    __slots__ = ("_instance", "_whitelist")

    # ----------------------------------------------------------------
    # ctor
    # ----------------------------------------------------------------
    def __init__(
        self,
        svc_or_cls: Union[type[S], S],
        *,
        extra_allowed: Set[str] | None = None,
    ) -> None:
        klass, instance = self._normalize(svc_or_cls)

        # methods declared *only* in the concrete class
        whitelist = self._own_methods(klass)
        if extra_allowed:
            whitelist.update(extra_allowed)

        self._whitelist: Set[str] = whitelist
        self._instance: S = instance

    # ----------------------------------------------------------------
    # public API
    # ----------------------------------------------------------------
    def __getattr__(self, name: str) -> Any:
        """Block everything that is not on the whitelist."""
        if name not in self._whitelist:
            logging.warning(
                "Blocked call to '%s' on %s (allowed: %s)",
                name,
                self._instance.__class__.__name__,
                ", ".join(sorted(self._whitelist)),
            )
            raise AttributeError(
                f"'{name}' is not allowed; available: {sorted(self._whitelist)}"
            )
        return getattr(self._instance, name)

    def __dir__(self) -> list[str]:
        """`dir(wrapper)` shows only permitted names — handy in REPL/IDE."""
        return sorted(self._whitelist)

    def __repr__(self) -> str:
        cls_name = self._instance.__class__.__name__
        return f"<RoleServiceWrapper[{cls_name}] allowed={sorted(self._whitelist)}>"

    # Small helper for tests / diagnostics
    def allowed(self) -> Set[str]:
        """Return a *copy* of the current whitelist."""
        return set(self._whitelist)

    # ----------------------------------------------------------------
    # helpers
    # ----------------------------------------------------------------
    @staticmethod
    def _normalize(obj: Union[type[S], S]) -> tuple[type[S] | S, Any] | tuple[property, type[S] | S]:
        """Return `(class, instance)` whatever the caller provided."""
        if inspect.isclass(obj):
            return obj, obj()               # class → (class, instance)
        return obj.__class__, obj           # instance → (class, same instance)

    @staticmethod
    def _own_methods(klass: type[S]) -> Set[str]:
        """Methods defined **only** in this class (no parents, no dunders)."""
        return {
            name
            for name, val in klass.__dict__.items()
            if callable(val) and not name.startswith("__")
        }
