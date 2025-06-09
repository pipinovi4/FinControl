from .base   import ClientBase
from .create import ClientCreate
from .update import ClientUpdate
from .out    import ClientOut

class ClientSchema:
    Base   = ClientBase
    Create = ClientCreate
    Update = ClientUpdate
    Out    = ClientOut
