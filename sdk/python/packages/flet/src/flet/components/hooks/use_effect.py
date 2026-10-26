import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from flet.components.hooks.hook import Hook
from flet.components.utils import current_component


# eq=False: see ComponentOwned - lifecycle objects compare by identity.
@dataclass(eq=False)
class EffectHook(Hook):
    """
    Hook state container backing :func:`~flet.use_effect`.

    Stores effect callbacks, dependency snapshots, and runtime task handles used
    to schedule async setup/cleanup work across mount, update, and unmount
    phases.
    """

    setup: Callable[[], Any | Awaitable[Any]]
    cleanup: Callable[[], Any | Awaitable[Any]] | None = None
    _returned_cleanup: Callable[[], Any | Awaitable[Any]] | None = None
    """The cleanup the last non-`async` setup run returned, if any."""

    deps: list[Any] | None = None
    prev_deps: list[Any] | None = None

    _setup_task: asyncio.Task | None = None
    """The task running the last `async` setup, cancelled when the effect re-runs or
    the component unmounts."""

    _cleanup_task: asyncio.Task | None = None
    """The task finishing the effect's last cleanups, when one of them is `async`.
    Until it has finished and the effect's waiting setups and cleanups have run,
    new ones wait in `_queued`."""

    _queued: list[Callable[[], Any | Awaitable[Any]] | None] = field(
        default_factory=list
    )
    """Setups and cleanups waiting for `_cleanup_task`, in the order they were
    scheduled: a setup as the setup function it was scheduled with, a cleanup as
    `None`."""

    _active: bool = False
    """Whether a setup has run since the last cleanup, so there is something to
    clean up."""

    def has_cleanup(self) -> bool:
        """
        Whether the effect has a cleanup to run: one its setup returned, the
        `cleanup` argument, or both.
        """
        return callable(self._returned_cleanup) or callable(self.cleanup)

    def has_lifecycle_work(self) -> bool:
        """
        Whether unmounting has work to do: a cleanup to run, or a setup task still
        running to cancel.
        """
        return self.has_cleanup() or (
            self._setup_task is not None and not self._setup_task.done()
        )

    def take_cleanups(self) -> list[Callable[[], Any | Awaitable[Any]]]:
        """
        Returns the cleanups to run, in order: the one the last setup returned, then
        the `cleanup` argument.

        The returned cleanup belongs to the setup run that returned it, so it is
        forgotten here and runs only once.
        """
        cleanups = [c for c in (self._returned_cleanup, self.cleanup) if callable(c)]
        self._returned_cleanup = None
        return cleanups

    def running_cleanup(self) -> asyncio.Task | None:
        """
        Returns the task finishing the effect's last cleanups, until it has finished
        and the setups and cleanups waiting for it have run.
        """
        return self._cleanup_task

    def is_live(self) -> bool:
        """
        Whether the effect still belongs to a mounted component: it hasn't unmounted
        and hasn't been replaced by a remount.
        """
        component = self.component
        return (
            component is not None
            and component._state.mounted
            and self in component._state.hooks
        )

    def take_queued(self) -> list[Callable[[], Any | Awaitable[Any]] | None]:
        """
        Returns what to run of the setups and cleanups that waited for the effect's
        cleanups, in `_queued`'s form: one cleanup if any was queued, then the last
        setup if it came last. Earlier setups never ran and were superseded, so
        there is nothing to run them for. No setup is returned once the effect
        isn't live (see `is_live()`).
        """
        queued, self._queued = self._queued, []
        ops: list[Callable[[], Any | Awaitable[Any]] | None] = []
        if any(op is None for op in queued):
            ops.append(None)
        if queued and queued[-1] is not None and self.is_live():
            ops.append(queued[-1])
        return ops

    def cancel_setup(self):
        """
        Cancels the last setup task, if it is still running.

        A running cleanup task is left to finish. Safe to call repeatedly.
        """
        if self._setup_task and not self._setup_task.done():
            self._setup_task.cancel()


def use_effect(
    setup: Callable[[], Any | Awaitable[Any]],
    dependencies: Sequence[Any] | None = None,
    cleanup: Callable[[], Any | Awaitable[Any]] | None = None,
):
    """
    Perform side effects in function components.

    Args:
        setup: A function that performs the side effect. A non-`async` setup may
            return a cleanup function, which runs at the same times as `cleanup`,
            just before it. An `async` setup's return value is not used: pass
            `cleanup` instead. An `async` setup still running when the effect
            re-runs or the component unmounts is cancelled.
        dependencies: Values the effect depends on. The effect always runs after the
            component mounts. If absent, it also re-runs after every render. If
            empty, it runs only on mount. Otherwise, it re-runs only when one of the
            dependencies has changed.
        cleanup: An optional function that cleans up after the effect. It is run
            before the effect is re-run, and when the component unmounts. It may be
            `async`. The effect's cleanups always finish, in order, before its setup
            runs again.
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
