# schemas/user/__init__.py
from .base import UserBase
from .create import UserCreate
from .update import UserUpdate
from .out import UserOut


class UserSchema:
    Base = UserBase
    Create = UserCreate
    Update = UserUpdate
    Out = UserOut