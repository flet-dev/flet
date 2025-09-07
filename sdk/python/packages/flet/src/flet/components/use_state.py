from collections.abc import Callable
from typing import Any, TypeVar

from flet.components.component import current_component
from flet.components.hooks import StateHook
from flet.components.observable import Observable

StateT = TypeVar("StateT")


def use_state(initial: StateT) -> tuple[StateT, Callable[[StateT], None]]:
    component = current_component()
    hook = component.use_hook(lambda: StateHook(initial))

    def update_subscriptions(hook: StateHook):
        if callable(hook.disposer):
            component._detach_subscription(hook.disposer)
            hook.disposer = None
        if isinstance(hook.value, Observable):
            hook.disposer = component._attach_subscription(hook.value)
        else:
            hook.disposer = None

    update_subscriptions(hook)

    def set_state(new_value: Any):
        # shallow equality; swap to "is" or custom comparator if needed
        if new_value != hook.value:
            hook.value = new_value
            update_subscriptions(hook)
            hook.version += 1
            component._schedule_update()

    return hook.value, set_state
