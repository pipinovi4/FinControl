from .base   import AdminBase
from .create import AdminCreate
from .update import AdminUpdate
from .out    import AdminOut

class AdminSchema:
    Base   = AdminBase
    Create = AdminCreate
    Update = AdminUpdate
    Out    = AdminOut
