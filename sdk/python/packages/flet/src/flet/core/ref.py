import weakref
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
__all__ = ["Ref"]


class Ref(Generic[T]):
    def __init__(self):
        self._current: Optional[weakref.ref[T]] = None

    @property
    def current(self) -> Optional[T]:
        return self._current() if self._current is not None else None

    @current.setter
    def current(self, value: T):
        self._current = weakref.ref(value)
