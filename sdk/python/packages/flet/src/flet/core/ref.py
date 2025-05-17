from typing import Generic, TypeVar

T = TypeVar("T")


class Ref(Generic[T]):
    def __init__(self, value: T = None):
        self._current: T = value

    @property
    def current(self) -> T:
        return self._current

    @current.setter
    def current(self, value: T):
        self._current = value
