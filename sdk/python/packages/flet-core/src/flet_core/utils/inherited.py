from typing import Generic, TypeVar

T = TypeVar('T')

class Inherited(Generic[T], T): ...
