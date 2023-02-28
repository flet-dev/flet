from typing import Generic, TypeVar, Optional, List, Any

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

    @property
    def previous_children(self) -> Optional[List[Any]]:
        return self._current._Control__previous_children

