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
            cleanup=lambda: None,
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
