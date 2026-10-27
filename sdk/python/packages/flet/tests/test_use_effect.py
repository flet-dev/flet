import asyncio
import gc
import sys
import weakref
from datetime import datetime, timezone

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
        self.component._state.mounted = False
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
    async def test_setup_waits_for_async_cleanup(self, runner):
        """A dependency change runs the setup again only after an `async` cleanup has
        finished."""
        log: list[str] = []

        async def cleanup():
            await asyncio.sleep(0)
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

        assert log == ["setup 1", "cleanup", "setup 2"]

    @pytest.mark.asyncio
    async def test_cleanups_finish_in_order_before_setup_reruns(self, runner):
        """An `async` returned cleanup finishes before a non-`async` `cleanup`
        argument runs, and both before the setup runs again."""
        log: list[str] = []

        def make_setup(tag):
            def setup():
                log.append(f"setup {tag}")

                async def flush():
                    await asyncio.sleep(0)
                    log.append(f"flush {tag}")

                return flush

            return setup

        def close():
            log.append("close")

        await runner.mount(
            lambda: use_effect_module.use_effect(make_setup("1"), [1], close)
        )
        await runner.rerender(
            lambda: use_effect_module.use_effect(make_setup("2"), [2], close)
        )

        assert log == ["setup 1", "flush 1", "close", "setup 2"]

    @pytest.mark.asyncio
    async def test_async_cleanup_finishes_when_nothing_else_references_it(self, runner):
        """An `async` cleanup finishes even when nothing else references it across a
        garbage collection."""
        log: list[str] = []
        gates: list[weakref.ref[asyncio.Future]] = []

        def make_setup(tag):
            def setup():
                log.append(f"setup {tag}")

                async def cleanup():
                    gate = asyncio.get_running_loop().create_future()
                    gates.append(weakref.ref(gate))
                    await gate
                    log.append(f"cleanup {tag}")

                return cleanup

            return setup

        await runner.mount(lambda: use_effect_module.use_effect(make_setup("1"), [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(make_setup("2"), [2])
        )

        gc.collect()
        (gate,) = [g for ref in gates if (g := ref()) is not None]
        gate.set_result(None)
        await asyncio.sleep(0.01)

        assert log == ["setup 1", "cleanup 1", "setup 2"]
        assert not runner.session._Session__effect_cleanup_tasks

    @pytest.mark.asyncio
    async def test_setup_superseded_while_waiting_never_runs(self, runner):
        """A setup still waiting for cleanups when the effect re-runs again is
        skipped, and only the latest setup runs."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(lambda: log.append("setup 2"), [2])
        )
        await runner.rerender(
            lambda: use_effect_module.use_effect(lambda: log.append("setup 3"), [3])
        )
        release.set()
        await asyncio.sleep(0.01)

        assert log == ["setup 1", "cleanup 1", "setup 3"]

    @pytest.mark.asyncio
    async def test_unmount_cancels_setup_waiting_for_cleanups(self, runner):
        """Unmounting while a setup waits for cleanups means it never runs."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(lambda: log.append("setup 2"), [2])
        )
        await runner.unmount()
        release.set()
        await asyncio.sleep(0.01)

        assert log == ["setup 1", "cleanup 1"]

    @pytest.mark.asyncio
    async def test_cleanup_argument_runs_once_per_setup_while_cleanups_wait(
        self, runner
    ):
        """Re-renders during a slow cleanup don't run the `cleanup` argument again
        for setups that never ran."""
        log: list[str] = []
        release = asyncio.Event()

        def setup():
            log.append("setup")

            async def flush():
                await release.wait()
                log.append("flush")

            return flush

        def close():
            log.append("close")

        def body():
            use_effect_module.use_effect(setup, None, close)

        await runner.mount(body)
        for _ in range(3):
            await runner.rerender(body)
        release.set()
        await asyncio.sleep(0.01)

        assert log == ["setup", "flush", "close", "setup"]

    @pytest.mark.asyncio
    async def test_back_to_back_setups_run_the_cleanup_between(self, runner):
        """Two setups scheduled before the effect loop runs still run the first
        one's cleanup between them."""
        log: list[str] = []
        runs = iter(["1", "2"])

        def setup():
            tag = next(runs)
            log.append(f"setup {tag}")
            return lambda: log.append(f"cleanup {tag}")

        runner._render(lambda: use_effect_module.use_effect(setup))
        runner.component._state.mounted = True
        (hook,) = runner.component._state.hooks
        runner.session.schedule_effect(hook, False)
        runner.session.schedule_effect(hook, False)
        await runner._drain()

        assert log == ["setup 1", "cleanup 1", "setup 2"]

    @pytest.mark.asyncio
    async def test_waiting_setup_never_runs_after_unmount_while_disconnected(
        self, runner
    ):
        """A setup waiting for cleanups doesn't run once the component has unmounted,
        even when the session was disconnected and dropped the unmount cleanup."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(lambda: log.append("setup 2"), [2])
        )
        runner.session._Session__conn = None
        runner.session._Session__expires_at = datetime.now(timezone.utc)
        await runner.unmount()
        release.set()
        await asyncio.sleep(0.01)

        assert log == ["setup 1", "cleanup 1"]

    @pytest.mark.asyncio
    async def test_unmount_as_cleanups_finish_skips_the_waiting_setup(self, runner):
        """Unmounting just as slow cleanups finish means the setup waiting for them
        never runs."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        def setup_2():
            log.append("setup 2")
            return lambda: log.append("cleanup 2")

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(lambda: use_effect_module.use_effect(setup_2, [2]))
        release.set()
        runner.component._state.mounted = False
        runner.component._run_unmount_effects()
        await runner._drain()

        assert log == ["setup 1", "cleanup 1"]

    @pytest.mark.asyncio
    async def test_render_as_cleanups_finish_runs_the_latest_setup_once(self, runner):
        """A render just as slow cleanups finish runs only its own setup, once."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        def make_setup(tag):
            def setup():
                log.append(f"setup {tag}")
                return lambda: log.append(f"cleanup {tag}")

            return setup

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(make_setup("2"), [2])
        )
        release.set()
        runner._render(lambda: use_effect_module.use_effect(make_setup("3"), [3]))
        runner.component._run_render_effects()
        await runner._drain()

        assert log == ["setup 1", "cleanup 1", "setup 3"]

    @pytest.mark.asyncio
    async def test_each_render_runs_its_own_setup_once(self, runner):
        """A render landing between slow cleanups finishing and the waiting setup
        running doesn't run its setup twice: each render's setup runs once, in
        order."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        def make_setup(tag):
            def setup():
                log.append(f"setup {tag}")
                return lambda: log.append(f"cleanup {tag}")

            return setup

        def render_3():
            runner._render(lambda: use_effect_module.use_effect(make_setup("3"), [3]))
            runner.component._run_render_effects()

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(make_setup("2"), [2])
        )
        release.set()
        asyncio.get_running_loop().call_soon(render_3)
        await runner._drain()

        assert log.count("setup 3") == 1
        assert log[:2] == ["setup 1", "cleanup 1"]
        assert log[-1] == "setup 3"

    @pytest.mark.asyncio
    async def test_waiting_setup_never_runs_after_the_session_closes(self, runner):
        """A setup waiting for cleanups doesn't run once the session has closed."""
        log: list[str] = []
        release = asyncio.Event()

        async def first_cleanup():
            await release.wait()
            log.append("cleanup 1")

        def setup_1():
            log.append("setup 1")
            return first_cleanup

        await runner.mount(lambda: use_effect_module.use_effect(setup_1, [1]))
        await runner.rerender(
            lambda: use_effect_module.use_effect(lambda: log.append("setup 2"), [2])
        )
        runner.session._Session__closed = True
        release.set()
        await asyncio.sleep(0.01)

        assert log == ["setup 1", "cleanup 1"]

    @pytest.mark.asyncio
    async def test_quick_mount_and_unmount_runs_setup_then_cleanup(self, runner):
        """A component unmounted before its effects ran still runs the setup, then
        the cleanup, once each."""
        log: list[str] = []

        runner._render(
            lambda: use_effect_module.use_effect(
                lambda: log.append("setup"), [], cleanup=lambda: log.append("cleanup")
            )
        )
        runner.component._state.mounted = True
        runner.component._run_mount_effects()
        runner.component._state.mounted = False
        runner.component._run_unmount_effects()
        await runner._drain()

        assert log == ["setup", "cleanup"]

    @pytest.mark.asyncio
    async def test_setup_running_after_unmount_is_cleaned_up_right_away(self, runner):
        """A setup that runs after its component unmounted, with no cleanup
        scheduled, is cleaned up right away."""
        log: list[str] = []
        runs = iter(["1", "2"])

        def setup():
            tag = next(runs)
            log.append(f"setup {tag}")
            return lambda: log.append(f"cleanup {tag}")

        await runner.mount(lambda: use_effect_module.use_effect(setup, [1]))
        (hook,) = runner.component._state.hooks
        runner.component._state.mounted = False
        runner.component._state.hooks.clear()
        runner.session.schedule_effect(hook, False)
        await runner._drain()

        assert log == ["setup 1", "cleanup 1", "setup 2", "cleanup 2"]

    @pytest.mark.asyncio
    async def test_cancelled_error_from_a_cleanup_keeps_effects_running(self, runner):
        """A cleanup raising `CancelledError` counts as cancelled, not failed, and
        the effect's setup and later effects still run."""
        log: list[str] = []

        def make_setup(tag):
            def setup():
                log.append(f"setup {tag}")

                async def cleanup():
                    log.append(f"async cleanup {tag}")

                return cleanup

            return setup

        def cancelled_cleanup():
            raise asyncio.CancelledError

        for i, deps in enumerate(([1], [2], [3])):
            body = lambda deps=deps: use_effect_module.use_effect(  # noqa: E731
                make_setup(deps[0]), deps, cancelled_cleanup
            )
            await (runner.mount(body) if i == 0 else runner.rerender(body))

        assert log == [
            "setup 1",
            "async cleanup 1",
            "setup 2",
            "async cleanup 2",
            "setup 3",
        ]
        assert runner.errors == []

    @pytest.mark.asyncio
    async def test_cancelled_async_cleanup_does_not_skip_the_other(self, runner):
        """An `async` cleanup that gets cancelled doesn't keep the other `async`
        cleanup from running."""
        log: list[str] = []

        def setup():
            async def cleanup():
                future = asyncio.get_running_loop().create_future()
                future.cancel()
                await future

            return cleanup

        async def cleanup_argument():
            log.append("cleanup argument")

        await runner.mount(
            lambda: use_effect_module.use_effect(setup, [], cleanup_argument)
        )
        await runner.unmount()

        assert log == ["cleanup argument"]
        assert runner.errors == []

    @pytest.mark.asyncio
    async def test_async_cleanups_run_one_after_the_other(self, runner):
        """The `cleanup` argument starts only once an `async` returned cleanup has
        finished."""
        log: list[str] = []

        def setup():
            async def flush():
                for _ in range(3):
                    await asyncio.sleep(0)
                log.append("flushed")

            return flush

        async def close():
            log.append("closed")

        await runner.mount(lambda: use_effect_module.use_effect(setup, [], close))
        await runner.unmount()

        assert log == ["flushed", "closed"]

    @pytest.mark.asyncio
    async def test_async_cleanup_failure_is_reported_while_the_other_runs(self, runner):
        """An `async` cleanup that raises is reported without waiting for the
        cleanup after it, which may never finish."""

        def setup():
            async def cleanup():
                raise RuntimeError("cleanup failed")

            return cleanup

        async def hanging_cleanup():
            await asyncio.get_running_loop().create_future()

        await runner.mount(
            lambda: use_effect_module.use_effect(setup, [], hanging_cleanup)
        )
        await runner.unmount()

        assert len(runner.errors) == 1
        assert "cleanup failed" in runner.errors[0]
        for task in runner.session._Session__effect_cleanup_tasks:
            task.cancel()

    @pytest.mark.skipif(sys.version_info < (3, 11), reason="needs Task.cancelling()")
    @pytest.mark.asyncio
    async def test_cancelling_cleanups_skips_the_ones_not_reached(self, runner):
        """Cancelling the task finishing `async` cleanups skips the ones it hasn't
        reached."""
        log: list[str] = []

        def setup():
            async def cleanup():
                await asyncio.get_running_loop().create_future()

            return cleanup

        async def cleanup_argument():
            log.append("cleanup argument")

        await runner.mount(
            lambda: use_effect_module.use_effect(setup, [], cleanup_argument)
        )
        await runner.unmount()
        (task,) = runner.session._Session__effect_cleanup_tasks
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert log == []
        assert runner.errors == []

    @pytest.mark.asyncio
    async def test_async_cleanup_return_value_is_ignored(self, runner):
        """An `async` cleanup returning an exception object isn't reported."""

        async def cleanup():
            return RuntimeError("just a value")

        await runner.mount(
            lambda: use_effect_module.use_effect(lambda: None, [], cleanup)
        )
        await runner.unmount()

        assert runner.errors == []

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
