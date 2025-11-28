import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

from flet.components.hooks.hook import Hook
from flet.components.utils import current_component


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
    """
    Perform side effects in function components.

    Args:
        setup: A function that performs the side effect. It may optionally return
            a cleanup function.
        dependencies: If present, the effect is only re-run when one of the dependencies
            has changed. If absent, the effect is only run on initial render.
        cleanup: An optional function that cleans up after the effect. It is run
            before the effect is re-run, and when the component unmounts.
    """
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


def on_mounted(fn: Callable[[], Any | Awaitable[Any]]) -> None:
    """
    Run exactly once after the component mounts.

    Args:
        fn (Callable[[], Any | Awaitable[Any]]): A function to run after the component
            mounts.
    """
    use_effect(fn, dependencies=[])


def on_unmounted(fn: Callable[[], Any | Awaitable[Any]]) -> None:
    """
    Run exactly once when the component unmounts.

    Args:
        fn (Callable[[], Any | Awaitable[Any]]): A function to run when the component
            unmounts.
    """
    # No-op setup; only need cleanup to fire on unmount
    use_effect(lambda: None, dependencies=[], cleanup=fn)


def on_updated(
    fn: Callable[[], Any | Awaitable[Any]], dependencies: Sequence[Any] | None = None
) -> None:
    """
    Run after each post-mount render (or when dependencies change).
    With dependencies=None this fires every update; with dependencies=[...] only
    on changes.

    Args:
        fn (Callable[[], Any | Awaitable[Any]]): A function to run after each
            post-mount render (or when dependencies change).
        dependencies (Sequence[Any] | None): If present, `fn` is only run when one
            of the dependencies has changed. If absent, `fn` is run after every
            render.
    """
    use_effect(fn, dependencies=dependencies)


on_mounted = on_mounted  # alias
on_unmounted = on_unmounted  # alias
on_updated = on_updated  # alias
