import asyncio

import pytest

import flet.components.hooks.use_effect as use_effect_module
from flet.components.component import Component
from flet.components.hooks.use_effect import EffectHook


def test_render_effect_changed_deps_runs_cleanup_then_setup_once_each():
    c = Component(fn=lambda: None, args=(), kwargs={})
    c._state.mounted = True
    calls: list[bool] = []
    c._schedule_effect = lambda hook, is_cleanup=False: calls.append(is_cleanup)  # type: ignore[method-assign]

    c._state.hooks = [
        EffectHook(
            c,
            setup=lambda: None,
            _returned_cleanup=lambda: None,
            deps=[2],
            prev_deps=[1],
        )
    ]

    c._run_render_effects()

    assert calls == [True, False]


def test_render_effect_unchanged_deps_schedules_nothing():
    c = Component(fn=lambda: None, args=(), kwargs={})
    c._state.mounted = True
    calls: list[bool] = []
    c._schedule_effect = lambda hook, is_cleanup=False: calls.append(is_cleanup)  # type: ignore[method-assign]

    c._state.hooks = [
        EffectHook(
            c,
            setup=lambda: None,
            cleanup=lambda: None,
            deps=[1],
            prev_deps=[1],
        )
    ]

    c._run_render_effects()

    assert calls == []


def test_will_unmount_releases_cached_render_references():
    c = Component(fn=lambda: None, args=(1, 2, 3), kwargs={"k": "v"})
    c._state.mounted = True
    c._b = ["body"]
    c._state.last_b = ["memo-body"]
    c._state.last_args = ("a", "b")
    c._state.last_kwargs = {"x": "y"}
    c._contexts = {object(): object()}

    c.will_unmount()

    assert c._b is None
    assert c._state.last_b is None
    assert c._state.last_args == ()
    assert c._state.last_kwargs == {}
    assert c._contexts == {}


def test_use_effect_retains_setup_returned_cleanup_across_renders(monkeypatch):
    c = Component(fn=lambda: None, args=(), kwargs={})

    def cleanup():
        return None

    def setup():
        return cleanup

    monkeypatch.setattr(use_effect_module, "current_component", lambda: c)

    use_effect_module.use_effect(setup, dependencies=[])
    hook = c._state.hooks[0]
    hook._returned_cleanup = cleanup

    c._state.hook_cursor = 0
    use_effect_module.use_effect(setup, dependencies=[])

    assert hook._returned_cleanup is cleanup


def test_unmount_schedules_returned_cleanup():
    c = Component(fn=lambda: None, args=(), kwargs={})
    c._state.mounted = True
    calls: list[bool] = []
    c._schedule_effect = lambda hook, is_cleanup=False: calls.append(is_cleanup)  # type: ignore[method-assign]
    hook = EffectHook(c, setup=lambda: None, _returned_cleanup=lambda: None)
    c._state.hooks = [hook]

    c._run_unmount_effects()

    assert calls == [True]


@pytest.mark.asyncio
async def test_unmount_schedules_cleanup_for_pending_setup_task():
    c = Component(fn=lambda: None, args=(), kwargs={})
    c._state.mounted = True
    calls: list[bool] = []
    c._schedule_effect = lambda hook, is_cleanup=False: calls.append(is_cleanup)  # type: ignore[method-assign]
    task = asyncio.create_task(asyncio.sleep(60))
    hook = EffectHook(c, setup=lambda: None)
    hook._setup_task = task
    c._state.hooks = [hook]

    c._run_unmount_effects()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert calls == [True]
