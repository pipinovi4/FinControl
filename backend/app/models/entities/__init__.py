"""
Entities package initializer.

This module re-exports all core domain entity classes so that they can be
imported directly from 'backend.app.models.entities'.
"""

# Core user entities
from backend.app.models.entities.user import User
from backend.app.models.entities.client import Client
from backend.app.models.entities.worker import Worker
from backend.app.models.entities.broker import Broker
from backend.app.models.entities.admin import Admin

# Public API of the entities package
__all__ = [
    "User",
    "Client",
    "Worker",
    "Broker",
    "Admin",
]
