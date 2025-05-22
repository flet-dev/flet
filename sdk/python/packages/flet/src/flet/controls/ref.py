import weakref
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
__all__ = ["Ref"]


class Ref(Generic[T]):
    def __init__(self, value: T = None):
        self._current: Optional[weakref.ref[T]] = weakref.ref(value) if value is not None else None

    @property
    def current(self) -> Optional[T]:
        return self._current() if self._current is not None else None

    @current.setter
    def current(self, value: Optional[T]):
        self._current = weakref.ref(value) if value is not None else None
