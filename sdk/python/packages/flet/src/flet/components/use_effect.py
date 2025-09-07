from collections.abc import Callable
from typing import Any

from flet.components.component import _current_component
from flet.components.hooks import EffectHook


def use_effect(fn: Callable[[], Any], deps: list[Any] | None = None):
    component = _current_component()
    hook = component.use_hook(lambda: EffectHook(fn=fn, deps=deps))

    # update effect hook
    hook.fn = fn
    hook.prev_deps = hook.deps
    hook.deps = deps
