import asyncio

import pytest
import pytest_asyncio

import flet.components.hooks.use_effect as use_effect_module
from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class EffectRunner:
    """A component with a session effect loop, rendered by hand."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch):
        conn = Connection()
        conn.pubsubhub = PubSubHub()
        self.session = Session(conn)
        self.errors: list[str] = []
        self.session.error = self.errors.append  # type: ignore[method-assign]
        self.component = Component(fn=lambda: None, args=(), kwargs={})
        self.component._schedule_effect = self.session.schedule_effect  # type: ignore[method-assign]
        monkeypatch.setattr(
            use_effect_module, "current_component", lambda: self.component
        )
        self.session.start_updates_scheduler()

    def _render(self, body):
        self.component._state.hook_cursor = 0
        body()

    async def _drain(self):
        for _ in range(3):
            self.session._Session__updates_ready.set()
            await asyncio.sleep(0.01)

    async def mount(self, body):
        self._render(body)
        self.component._state.mounted = True
        self.component._run_mount_effects()
        await self._drain()

    async def rerender(self, body):
        self._render(body)
        self.component._run_render_effects()
        await self._drain()

    async def unmount(self):
        self.component._run_unmount_effects()
        await self._drain()

    async def close(self):
        self.session._Session__closed = True
        self.session._Session__updates_ready.set()
        await self.session._Session__updates_task


@pytest_asyncio.fixture
async def runner(monkeypatch):
    r = EffectRunner(monkeypatch)
    yield r
    await r.close()


@pytest.fixture
def scheduled() -> tuple[Component, list[bool]]:
    """A mounted component that records what it schedules instead of running it."""
    c = Component(fn=lambda: None, args=(), kwargs={})
    c._state.mounted = True
    calls: list[bool] = []
    c._schedule_effect = lambda hook, is_cleanup=False: calls.append(is_cleanup)  # type: ignore[method-assign]
    return c, calls


def returning_cleanup(log: list[str], tag: str):
    def setup():
        log.append(f"setup {tag}")
        return lambda: log.append(f"cleanup {tag}")

    return setup


CLEANUP_KINDS = pytest.mark.parametrize(
    "cleanup_field", ["cleanup", "_returned_cleanup"], ids=["argument", "returned"]
)


class TestEffectScheduling:
    """What a component queues for its effects on re-render and unmount."""

    @CLEANUP_KINDS
    def test_changed_deps_schedule_cleanup_then_setup(self, scheduled, cleanup_field):
        """Changed dependencies queue the cleanup, then the setup, once each."""
        c, calls = scheduled
        c._state.hooks = [
            EffectHook(
                c,
                setup=lambda: None,
                deps=[2],
                prev_deps=[1],
                **{cleanup_field: lambda: None},
            )
        ]

        c._run_render_effects()

        assert calls == [True, False]

    def test_unchanged_deps_schedule_nothing(self, scheduled):
        """Unchanged dependencies queue nothing."""
        c, calls = scheduled
        c._state.hooks = [
            EffectHook(
                c, setup=lambda: None, cleanup=lambda: None, deps=[1], prev_deps=[1]
            )
        ]

        c._run_render_effects()

        assert calls == []

    @CLEANUP_KINDS
    def test_unmount_schedules_cleanup(self, scheduled, cleanup_field):
        """Unmounting queues the effect's cleanup."""
        c, calls = scheduled
        c._state.hooks = [
            EffectHook(c, setup=lambda: None, **{cleanup_field: lambda: None})
        ]

        c._run_unmount_effects()

        assert calls == [True]

    @pytest.mark.asyncio
    async def test_unmount_schedules_cleanup_for_running_setup_task(self, scheduled):
        """Unmounting queues a cleanup for an effect whose setup task still runs."""
        c, calls = scheduled
        task = asyncio.create_task(asyncio.sleep(60))
        hook = EffectHook(c, setup=lambda: None)
        hook._setup_task = task
        c._state.hooks = [hook]

        c._run_unmount_effects()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert calls == [True]


class TestEffectLoop:
    """Effects driven end-to-end: render, mount, re-render and unmount."""

    @pytest.mark.asyncio
    async def test_returned_cleanup_runs_on_unmount_after_rerender(self, runner):
        """A cleanup returned by the setup runs on unmount after a re-render."""
        log: list[str] = []
        setup = returning_cleanup(log, "a")

        def body():
            use_effect_module.use_effect(setup, [])

        await runner.mount(body)
        await runner.rerender(body)
        await runner.unmount()

        assert log == ["setup a", "cleanup a"]

    @pytest.mark.asyncio
    async def test_returned_cleanup_runs_before_setup_on_dependency_change(
        self, runner
    ):
        """A dependency change runs the returned cleanup before the setup re-runs."""
        log: list[str] = []

        await runner.mount(
            lambda: use_effect_module.use_effect(returning_cleanup(log, "1"), [1])
        )
        await runner.rerender(
            lambda: use_effect_module.use_effect(returning_cleanup(log, "2"), [2])
        )
        await runner.unmount()

        assert log == ["setup 1", "cleanup 1", "setup 2", "cleanup 2"]

    @pytest.mark.asyncio
    async def test_returned_cleanup_and_cleanup_argument_both_run(self, runner):
        """The returned cleanup runs first, then the `cleanup` argument."""
        log: list[str] = []

        await runner.mount(
            lambda: use_effect_module.use_effect(
                returning_cleanup(log, "returned"),
                [],
                cleanup=lambda: log.append("cleanup argument"),
            )
        )
        await runner.unmount()

        assert log == ["setup returned", "cleanup returned", "cleanup argument"]

    @pytest.mark.asyncio
    async def test_async_cleanup_runs_on_dependency_change(self, runner):
        """An `async` cleanup runs when a dependency change re-runs the setup."""
        log: list[str] = []

        async def cleanup():
            log.append("cleanup")

        await runner.mount(
            lambda: use_effect_module.use_effect(
                lambda: log.append("setup 1"), [1], cleanup
            )
        )
        await runner.rerender(
            lambda: use_effect_module.use_effect(
                lambda: log.append("setup 2"), [2], cleanup
            )
        )

        assert log == ["setup 1", "setup 2", "cleanup"]

    @pytest.mark.asyncio
    async def test_failing_cleanup_does_not_skip_the_other(self, runner):
        """A cleanup that raises is reported, and the other cleanup still runs."""
        log: list[str] = []

        def setup():
            def cleanup():
                raise RuntimeError("cleanup failed")

            return cleanup

        await runner.mount(
            lambda: use_effect_module.use_effect(
                setup, [], cleanup=lambda: log.append("cleanup argument")
            )
        )
        await runner.unmount()

        assert log == ["cleanup argument"]
        assert len(runner.errors) == 1
        assert "cleanup failed" in runner.errors[0]

    @pytest.mark.asyncio
    async def test_running_async_setup_is_cancelled_on_unmount(self, runner):
        """An `async` setup still running at unmount is cancelled."""
        log: list[str] = []

        async def setup():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                log.append("cancelled")
                raise

        def body():
            use_effect_module.use_effect(setup, [])

        await runner.mount(body)
        await runner.rerender(body)
        await runner.unmount()

        assert log == ["cancelled"]
