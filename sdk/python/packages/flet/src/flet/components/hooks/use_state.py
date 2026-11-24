from __future__ import annotations

import asyncio
import contextlib
import contextvars
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar, overload

from flet.components.hooks.hook import Hook
from flet.components.observable import Observable, ObservableSubscription
from flet.components.utils import current_component
from flet.utils.event_loop import running_loop

StateT = TypeVar("StateT")
Updater = Callable[[StateT], StateT]


# eq=False: see ComponentOwned - lifecycle objects compare by identity.
@dataclass(eq=False)
class StateHook(Hook):
    """
    Hook state container backing :func:`flet.use_state`.
    """

    value: Any
    """
    Current state value returned by :func:`flet.use_state`.

    Updated by the `set_state` setter. It may hold any Python value,
    including an :class:`~flet.Observable`.
    """

    subscription: ObservableSubscription | None = None
    """
    Active subscription bound to `value` when `value` is observable.

    Set by `update_subscription()` to track observable changes and schedule
    component updates. `None` when `value` is not an
    :class:`~flet.Observable` or after detachment.
    """

    version: int = 0
    """
    Monotonic revision counter for state replacements.

    Incremented each time `set_state` accepts a changed value. Used to mark
    hook-level updates even when consumers do not inspect `value` directly.
    """

    _loop: asyncio.AbstractEventLoop | None = field(default=None, repr=False)
    """The event loop the component renders on, where `set_state` called from
    another thread is applied. `None` when rendered without a running loop, as in
    synchronous tests."""

    _context: contextvars.Context | None = field(default=None, repr=False)
    """A copy of the context of the render that created the hook, with the page
    set, in which `set_state` called from another thread is applied."""


@overload
def use_state(
    initial: Callable[[], StateT],
) -> tuple[StateT, Callable[[StateT | Updater], None]]: ...


@overload
def use_state(
    initial: StateT | Callable[[], StateT],
) -> tuple[StateT, Callable[[StateT | Updater], None]]: ...


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

    def create_hook() -> StateHook:
        loop = running_loop()
        return StateHook(
            component,
            initial() if callable(initial) else initial,
            _loop=loop,
            _context=contextvars.copy_context() if loop is not None else None,
        )

    hook = component.use_hook(create_hook)

    def update_subscription(h: StateHook):
        """
        Refreshes observable subscription for the current state value.

        Detaches any previous subscription and, if `h.value` is an
        :class:`~flet.Observable`, attaches a new `ObservableSubscription`
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

    def apply_state(new_value_or_fn: StateT | Updater):
        """Applies a `set_state` call, on the event loop."""
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

    def set_state(new_value_or_fn: StateT | Updater):
        """
        Update the state value.

        Can be called with either:
          - a direct new value, or
          - a function that takes the current value and returns the next one.

        Safe to call from any thread: from a worker thread, such as a
        `page.run_thread()` handler, the update is applied on the event loop,
        in call order, so it can't race a render of the component.
        """
        # `set_state` must not reference itself: the cycle would leave every
        # render's setters to the garbage collector.
        loop = hook._loop
        if loop is not None and running_loop() is not loop:
            # RuntimeError: the loop closed, so the app is gone.
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(
                    apply_state, new_value_or_fn, context=hook._context
                )
            return
        apply_state(new_value_or_fn)

    return hook.value, set_state
