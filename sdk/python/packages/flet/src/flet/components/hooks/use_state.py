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
    """
    Hook state container backing [`use_state()`][flet.use_state].
    """

    value: Any
    """
    Current state value returned by [`use_state()`][flet.use_state].

    Updated by the `set_state` setter. It may hold any Python value,
    including an [`Observable`][flet.].
    """

    subscription: ObservableSubscription | None = None
    """
    Active subscription bound to `value` when `value` is observable.

    Set by `update_subscription()` to track observable changes and schedule
    component updates. `None` when `value` is not an
    [`Observable`][flet.] or after detachment.
    """

    version: int = 0
    """
    Monotonic revision counter for state replacements.

    Incremented each time `set_state` accepts a changed value. Used to mark
    hook-level updates even when consumers do not inspect `value` directly.
    """


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
        """
        Refreshes observable subscription for the current state value.

        Detaches any previous subscription and, if `h.value` is an
        [`Observable`][flet.], attaches a new [`ObservableSubscription`][flet.]
        owned by the current component.

        Args:
            h: The state hook whose subscription must be synchronized with
                its current `value`.
        """
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
