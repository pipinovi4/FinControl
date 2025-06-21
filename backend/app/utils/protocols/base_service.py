from typing import Protocol

class BaseService(Protocol):
    """
    Minimal surface that any service is expected to implement.
    Used for safe runtime wrappers and dependency validation.
    """
    ...
