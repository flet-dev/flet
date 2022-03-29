from typing import Generic, TypeVar

T = TypeVar("T")


class Ref(Generic[T]):
    def __init__(self):
        self._current: T = None

    @property
    def current(self) -> T:
        return self._current

    @current.setter
    def current(self, value: T):
        self._current = value
