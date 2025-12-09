from enum import Enum

class PermissionRole(str, Enum):
    """
    Enum class representing the role-based access levels within the system.

    Roles:
    - CLIENT: End user submitting applications via Telegram bot.
    - WORKER: Internal employee who processes and manages applications.
    - BROKER: Agent responsible for handling and filtering leads.
    - ADMIN: Full access to all system functionalities and user management.

    This enum is used across the system to enforce role-based permissions.
    """
    WORKER = 'WORKER'
    BROKER = 'BROKER'
    ADMIN = 'ADMIN'
