from .base    import AuthBase
from .create  import AuthCreate
from .out     import AuthOut
from .update import AuthUpdate


class AuthSchema:
    Base   = AuthBase
    Create = AuthCreate
    Out    = AuthOut
    Update = AuthUpdate
