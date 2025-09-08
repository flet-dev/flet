from collections.abc import Callable, Sequence
from typing import Any

from flet.components.component import current_component
from flet.components.hooks import EffectHook


def use_effect(
    setup: Callable[[], Any],
    dependencies: Sequence[Any] | None = None,
    cleanup: Callable[[], Any] | None = None,
):
    component = current_component()
    deps = list(dependencies) if dependencies is not None else None

    # get or create effect hook
    hook = component.use_hook(
        lambda: EffectHook(
            component,
            setup=setup,
            deps=deps,
            cleanup=cleanup,
        )
    )

    # update effect hook
    hook.setup = setup
    hook.prev_deps = hook.deps
    hook.deps = deps
    hook.cleanup = cleanup


def on_mounted(fn: Callable[[], Any]) -> None:
    """
    Run exactly once after the component mounts.
    """
    use_effect(fn, dependencies=[])


def on_unmounted(fn: Callable[[], Any]) -> None:
    """
    Run exactly once when the component unmounts.
    """
    # No-op setup; only need cleanup to fire on unmount
    use_effect(lambda: None, dependencies=[], cleanup=fn)


def on_updated(
    fn: Callable[[], Any], dependencies: Sequence[Any] | None = None
) -> None:
    """
    Run after each post-mount render (or when dependencies change).
    With dependencies=None this fires every update; with dependencies=[...] only
    on changes.
    """
    use_effect(fn, dependencies=dependencies)
