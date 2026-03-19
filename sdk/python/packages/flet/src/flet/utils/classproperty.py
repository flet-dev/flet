from typing import Any, Callable, TypeVar

T = TypeVar("T")


class classproperty:
    def __init__(self, func: Callable[[type[T]], Any]) -> None:
        self.fget = func

    def __get__(self, instance: T, owner: type[T]) -> Any:
        return self.fget(owner)
