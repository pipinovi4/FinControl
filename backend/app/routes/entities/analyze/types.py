# types.py
from typing import Tuple, Type
from backend.app.utils.protocols import BaseService
from backend.app.utils.protocols import BaseSchemaNamespace

RawTuple = Tuple[
    str,
    Type[BaseService], Type[BaseService],
    Type[BaseService], Type[BaseService],
    Type[BaseSchemaNamespace],
]
