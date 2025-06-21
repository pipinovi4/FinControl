from __future__ import annotations

import logging
from typing import Any, TypeVar, Union

from backend.app.services.entities import (
    AdminService, BrokerService, WorkerService, ClientService,
    AdminInterfaceService, BrokerInterfaceService, WorkerInterfaceService, ClientInterfaceService,
    AdminFilterService, BrokerFilterService, WorkerFilterService, ClientFilterService,
    AdminUtils, BrokerUtils, WorkerUtilsService, ClientUtilService
)

S = TypeVar("S", AdminService, BrokerService, WorkerService, ClientService)

class LimitedService:
    """
    Wraps a service class/instance so that ONLY the methods declared
    directly on the class (i.e. not inherited) are accessible.
    """

    def __init__(self, svc_or_cls: Union[type[S], S]) -> None:
        # Normalize input -> (class, instance)
        klass, instance = self._normalize(svc_or_cls)

        # Build a whitelist of methods defined *only* on this class
        self._whitelist: set[str] = self._own_methods(klass)
        self._instance: S = instance

    # ---------- public API -------------------------------------------

    def __getattr__(self, name: str) -> Any:
        """Intercept every attribute lookup and allow only whitelisted methods."""
        if name not in self._whitelist:
            logging.warning(
                "Blocked call to %s on %s",
                name,
                self._instance.__class__.__name__,
            )
            raise AttributeError(
                f"❌ Method '{name}' is not allowed in limited context "
                f"({self._instance.__class__.__name__})."
            )
        return getattr(self._instance, name)

    # Show only allowed methods in dir() – handy for Python shell / IDE autocomplete
    def __dir__(self) -> list[str]:
        return sorted(self._whitelist)

    def __repr__(self) -> str:  # For debugging convenience
        cls_name = self._instance.__class__.__name__
        return f"<LimitedService[{cls_name}] allowed={sorted(self._whitelist)}>"

    # ---------- helpers ----------------------------------------------

    @staticmethod
    def _normalize(obj: Union[type[S], S]) -> tuple[type[S], S]:
        """
        Return (class, instance) regardless of whether a class or an
        already-instantiated object was provided.
        """
        if isinstance(obj, type):
            return obj, obj()          # create an instance
        return obj.__class__, obj      # already an instance

    @staticmethod
    def _own_methods(klass: type) -> set[str]:
        """
        Return the set of method names defined ONLY on this class
        (i.e. excluding inherited members and dunder methods).
        """
        return {
            name
            for name, val in klass.__dict__.items()
            if callable(val) and not name.startswith("__")
        }
