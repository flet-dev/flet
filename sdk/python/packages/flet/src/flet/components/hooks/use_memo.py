from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from flet.components.hooks.hook import Hook
from flet.components.utils import current_component, shallow_compare_args

MemoValueT = TypeVar("MemoValueT")


@dataclass
class MemoHook(Hook, Generic[MemoValueT]):
    value: MemoValueT | None = None
    prev_deps: list[Any] | None = None


def use_memo(
    calculate_value: Callable[[], MemoValueT], dependencies: Sequence[Any] | None = None
) -> MemoValueT:
    """
    Memoize a computed value between renders.
    - deps is None: recompute every render
    - deps == []  : compute once (mount), keep forever
    - else        : recompute when any dep changes (Object.is-like compare)
    """
    component = current_component()

    def _create() -> MemoHook[MemoValueT]:
        h = MemoHook[MemoValueT](component)
        # If deps is None we recompute every render, so no need to preset prev_deps.
        if dependencies is None:
            h.value = calculate_value()
        return h

    hook = component.use_hook(_create)  # type: MemoHook[MemoValueT]

    if dependencies is None:
        # Always recompute
        hook.value = calculate_value()
        return hook.value  # type: ignore[return-value]

    if hook.prev_deps is None or not shallow_compare_args(hook.prev_deps, dependencies):
        hook.value = calculate_value()
        hook.prev_deps = list(dependencies)

    return hook.value  # type: ignore[return-value]


memo = use_memo  # alias for convenience
