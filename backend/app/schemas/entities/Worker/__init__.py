from .base   import WorkerBase
from .create import WorkerCreate
from .update import WorkerUpdate
from .out    import WorkerOut

class WorkerSchema:
    Base   = WorkerBase
    Create = WorkerCreate
    Update = WorkerUpdate
    Out    = WorkerOut
