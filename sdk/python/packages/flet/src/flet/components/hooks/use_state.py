from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from flet.components.hooks.hook import Hook
from flet.components.observable import Observable, ObservableSubscription
from flet.components.utils import current_component


@dataclass
class StateHook(Hook):
    value: Any
    subscription: ObservableSubscription | None = None
    version: int = 0


StateT = TypeVar("StateT")


def use_state(initial: StateT) -> tuple[StateT, Callable[[StateT], None]]:
    component = current_component()
    hook = component.use_hook(lambda: StateHook(component, initial))

    def update_subscription(hook: StateHook):
        if hook.subscription:
            component._detach_observable_subscription(hook.subscription)
            hook.subscription = None
        if isinstance(hook.value, Observable):
            hook.subscription = component._attach_observable_subscription(hook.value)

    update_subscription(hook)

    def set_state(new_value: Any):
        # shallow equality; swap to "is" or custom comparator if needed
        if new_value != hook.value:
            hook.value = new_value
            update_subscription(hook)
            hook.version += 1
            if hook.component:
                hook.component._schedule_update()

    return hook.value, set_state
