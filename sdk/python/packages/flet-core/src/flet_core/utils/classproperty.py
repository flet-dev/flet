from typing import TypeVar, Type, Any, Callable


T = TypeVar("T")


class classproperty:
    def __init__(self, func: Callable[[Type[T]], Any]) -> None:
        self.fget = func

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        return self.fget(owner)
