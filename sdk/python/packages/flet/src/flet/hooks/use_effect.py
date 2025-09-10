import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

from flet.components.utils import current_component
from flet.hooks.hook import Hook


@dataclass
class EffectHook(Hook):
    setup: Callable[[], Any | Awaitable[Any]]
    cleanup: Callable[[], Any | Awaitable[Any]] | None = None
    deps: list[Any] | None = None
    prev_deps: list[Any] | None = None

    # runtime
    _setup_task: asyncio.Task | None = None  # last scheduled setup task
    _cleanup_task: asyncio.Task | None = None  # last scheduled cleanup task

    def cancel(self):
        if self._setup_task and not self._setup_task.done():
            self._setup_task.cancel()
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()


def use_effect(
    setup: Callable[[], Any | Awaitable[Any]],
    dependencies: Sequence[Any] | None = None,
    cleanup: Callable[[], Any | Awaitable[Any]] | None = None,
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


def mounted(fn: Callable[[], Any | Awaitable[Any]]) -> None:
    """
    Run exactly once after the component mounts.
    """
    use_effect(fn, dependencies=[])


def unmounted(fn: Callable[[], Any | Awaitable[Any]]) -> None:
    """
    Run exactly once when the component unmounts.
    """
    # No-op setup; only need cleanup to fire on unmount
    use_effect(lambda: None, dependencies=[], cleanup=fn)


def updated(
    fn: Callable[[], Any | Awaitable[Any]], dependencies: Sequence[Any] | None = None
) -> None:
    """
    Run after each post-mount render (or when dependencies change).
    With dependencies=None this fires every update; with dependencies=[...] only
    on changes.
    """
    use_effect(fn, dependencies=dependencies)


effect = use_effect  # alias
mounted = mounted  # alias
unmounted = unmounted  # alias
updated = updated  # alias
