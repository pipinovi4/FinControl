"""
Entities package initializer.

This module re-exports all core domain entity classes so that they can be
imported directly from 'backend.app.models.entities'.
"""

# Core user entities
from .user import User
from .application import Application
from .worker import Worker
from .broker import Broker
from .admin import Admin
from .credit import Credit
from .registration_invite import RegistrationInvite
from .promotion import Promotion

# Public API of the entities package
__all__ = [
    "User",
    "Application",
    "Worker",
    "Broker",
    "Admin",
    "Credit",
    "RegistrationInvite",
    "Promotion"
]
