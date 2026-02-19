from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from flet.components.hooks.hook import Hook
from flet.components.utils import current_component

__all__ = ["MutableRef", "use_ref"]

RefValueT = TypeVar("RefValueT")


class MutableRef(Generic[RefValueT]):
    """A mutable holder whose identity stays stable across renders."""

    __slots__ = ("current",)

    def __init__(self, initial_value: RefValueT | None = None):
        self.current = initial_value


@dataclass
class RefHook(Hook, Generic[RefValueT]):
    """
    Hook state container backing [`use_ref()`][flet.use_ref].

    Stores the stable [`MutableRef`][flet.MutableRef] instance for a component so
    it can be reused across renders without triggering updates when `.current`
    changes.
    """

    ref: MutableRef[RefValueT]


def use_ref(
    initial_value: RefValueT | Callable[[], RefValueT] | None = None,
) -> MutableRef[RefValueT]:
    """
    Preserve a mutable value for the lifetime of the component without causing \
    re-renders.

    Args:
        initial_value: Optional value or callable returning the value assigned
            to `ref.current`.

    Returns:
        A `MutableRef` whose `.current` property can be read and written freely.
    """
    component = current_component()

    def resolve_initial() -> RefValueT | None:
        """
        Resolves the initial ref value from literal or lazy initializer.

        If `initial_value` is callable, it is invoked and its return value is
        used. Otherwise, `initial_value` is returned as-is.
        """
        return initial_value() if callable(initial_value) else initial_value

    hook = component.use_hook(
        lambda: RefHook(
            component,
            MutableRef(resolve_initial()),
        )
    )

    return hook.ref
