import enum


class UserRole(enum.Enum):
    """
    Enumeration of available user roles in the system.

    Each role defines a specific level of access and permissions:

    - CLIENT: End-user who submits applications; limited access.
    - WORKER: Internal employee who manages their own clients and applications.
    - BROKER: External partner with read-only access to data.
    - ADMIN: Full administrative access to all system functionality.
    """
    CLIENT = "client"  # Standard user working via Telegram bot
    WORKER = "worker"  # Internal staff with limited system access
    BROKER = "broker"  # External user with read-only access
    ADMIN = "admin"    # System administrator