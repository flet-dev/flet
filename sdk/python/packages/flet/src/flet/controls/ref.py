import weakref
from typing import Generic, Optional, TypeVar

T = TypeVar("T", covariant=True)
__all__ = ["Ref"]


class Ref(Generic[T]):
    """Utility class which allows defining a reference to a control."""

    def __init__(self, value: Optional[T] = None):
        self.current = value

    @property
    def current(self) -> Optional[T]:
        return self._ref() if self._ref else None

    @current.setter
    def current(self, value: Optional[T]):
        self._ref = weakref.ref(value) if value is not None else None

    def __call__(self) -> Optional[T]:
        return self.current
