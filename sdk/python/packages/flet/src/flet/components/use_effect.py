from collections.abc import Callable
from typing import Any

from flet.components.component import current_component
from flet.components.hooks import EffectHook


def use_effect(setup: Callable[[], Any], dependencies: list[Any] | None = None):
    component = current_component()
    hook = component.use_hook(
        lambda: EffectHook(component, setup=setup, deps=dependencies)
    )

    # update effect hook
    hook.setup = setup
    hook.prev_deps = hook.deps
    hook.deps = dependencies
