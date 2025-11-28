from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from flet.components.hooks.hook import Hook
from flet.components.observable import Observable, ObservableSubscription
from flet.components.utils import current_component

StateT = TypeVar("StateT")
Updater = Callable[[StateT], StateT]


@dataclass
class StateHook(Hook):
    value: Any
    subscription: ObservableSubscription | None = None
    version: int = 0


def use_state(
    initial: StateT | Callable[[], StateT],
) -> tuple[StateT, Callable[[StateT | Updater], None]]:
    """
    Adds state to a function component, similar to React's useState().

    The returned setter accepts either:
      - a new value, or
      - a function receiving the previous state and returning the next one.

    Args:
        initial: Initial state value or a function returning it.

    Returns:
        (value, set_value) tuple.
    """
    component = current_component()
    hook = component.use_hook(
        lambda: StateHook(
            component,
            initial() if callable(initial) else initial,
        )
    )

    def update_subscription(h: StateHook):
        # Detach previous subscription if any
        if h.subscription:
            component._detach_observable_subscription(h.subscription)
            h.subscription = None

        # Attach new subscription if value is Observable
        if isinstance(h.value, Observable):
            h.subscription = component._attach_observable_subscription(h.value)

    update_subscription(hook)

    def set_state(new_value_or_fn: StateT | Updater):
        """
        Update the state value.

        Can be called with either:
          - a direct new value, or
          - a function that takes the current value and returns the next one.
        """
        # Compute next value
        new_value = (
            new_value_or_fn(hook.value)
            if callable(new_value_or_fn)
            else new_value_or_fn
        )

        # Only trigger update if value changed (shallow equality)
        if new_value != hook.value:
            hook.value = new_value
            update_subscription(hook)
            hook.version += 1
            if hook.component:
                hook.component._schedule_update()

    return hook.value, set_state
