from .base   import BrokerBase
from .create import BrokerCreate
from .update import BrokerUpdate
from .out    import BrokerOut

class BrokerSchema:
    Base   = BrokerBase
    Create = BrokerCreate
    Update = BrokerUpdate
    Out    = BrokerOut
