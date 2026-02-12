"""
Tests for use_state hook behavior.

Reproduces issue https://github.com/flet-dev/flet/issues/6153:
App state persists across toggled components when using ft.use_state.
When toggling between two component trees that each hold their own
@ft.observable app instance, the UI shows state from the first app
even after switching to the second.
"""

from dataclasses import dataclass, field

import flet as ft
from flet.components.component import Component, Renderer
from flet.components.hooks.use_state import StateHook


@ft.observable
@dataclass
class User:
    first_name: str
    last_name: str


@ft.observable
@dataclass
class App:
    users: list[User] = field(default_factory=list)


@ft.observable
@dataclass
class DifferentApp:
    users: list[User] = field(default_factory=list)


def test_use_state_returns_stale_state_after_branch_toggle():
    """
    Reproduces flet-dev/flet#6153.

    A component function conditionally calls use_state with either
    App(...) or DifferentApp(...) depending on a toggle flag.

    After the first render (toggle=True), the hook at position 1
    stores an App instance. When the component re-renders with
    toggle=False, the hook at position 1 should ideally return a
    DifferentApp instance, but instead it returns the stale App
    instance from the first render.

    This test verifies that the bug exists: use_state returns the
    wrong (stale) state after toggling branches.
    """
    # Track what use_state returns across renders
    captured = {}

    def app_view_fn():
        toggle, set_toggle = ft.use_state(True)
        if toggle:
            app, _ = ft.use_state(
                App(
                    users=[
                        User("John", "Doe"),
                        User("Jane", "Doe"),
                        User("Foo", "Bar"),
                    ]
                )
            )
            captured["class_name"] = App.__name__
            captured["instance_class"] = app.__class__.__name__
            captured["users"] = [u.first_name for u in app.users]
            captured["app"] = app
            return ft.Text(f"Class {App.__name__} instance {app.__class__.__name__}")
        else:
            app2, _ = ft.use_state(
                DifferentApp(
                    users=[
                        User("Alice2", "Smith"),
                        User("Bob2", "Johnson"),
                    ]
                )
            )
            captured["class_name"] = DifferentApp.__name__
            captured["instance_class"] = app2.__class__.__name__
            captured["users"] = [u.first_name for u in app2.users]
            captured["app"] = app2
            return ft.Text(
                f"Class {DifferentApp.__name__} instance {app2.__class__.__name__}"
            )

    app_view_fn.__is_component__ = True

    # Create a Component to hold state
    comp = Component(fn=app_view_fn, args=(), kwargs={})

    # First render: toggle=True, should use App
    renderer = Renderer(comp)
    renderer.render(app_view_fn)

    assert captured["class_name"] == "App"
    assert captured["instance_class"] == "App"
    assert captured["users"] == ["John", "Jane", "Foo"]
    assert isinstance(captured["app"], App)

    # Now simulate toggling: set the hook value for toggle (hook index 0) to False
    assert len(comp._state.hooks) == 2
    toggle_hook = comp._state.hooks[0]
    assert isinstance(toggle_hook, StateHook)
    assert toggle_hook.value is True
    toggle_hook.value = False

    # Re-render with toggle=False - should use DifferentApp
    comp._state.hook_cursor = 0
    renderer2 = Renderer(comp)
    renderer2.render(app_view_fn)

    # BUG: After toggling, the use_state at position 1 returns the OLD App
    # instance instead of creating a new DifferentApp instance.
    # Expected: instance_class == "DifferentApp", users == ["Alice2", "Bob2"]
    # Actual (bug): instance_class == "App", users == ["John", "Jane", "Foo"]

    # The class name is correctly "DifferentApp" because that's hardcoded
    assert captured["class_name"] == "DifferentApp"

    # The instance class should be "DifferentApp" but due to the bug it's "App"
    assert captured["instance_class"] == "App", (
        "BUG REPRODUCED: use_state returns stale App instance instead of "
        "DifferentApp after toggling branches"
    )

    # The users should be ["Alice2", "Bob2"] but due to the bug they are
    # ["John", "Jane", "Foo"] from the first App instance
    assert captured["users"] == ["John", "Jane", "Foo"], (
        "BUG REPRODUCED: users from the first App persist after toggling"
    )

    # The app instance should be a DifferentApp, but it's an App
    assert isinstance(captured["app"], App), (
        "BUG REPRODUCED: returned instance is App, not DifferentApp"
    )
    assert not isinstance(captured["app"], DifferentApp), (
        "BUG REPRODUCED: returned instance is not a DifferentApp"
    )


def test_use_state_hook_count_unchanged_after_branch_toggle():
    """
    Reproduces flet-dev/flet#6153.

    Verifies that the number of hooks does not grow when re-rendering
    with a different branch. The hook at position 1 is reused (not
    created anew), which is the root cause of the stale state issue.
    """

    def app_view_fn():
        toggle, _ = ft.use_state(True)
        if toggle:
            ft.use_state(App(users=[User("John", "Doe")]))
        else:
            ft.use_state(DifferentApp(users=[User("Alice2", "Smith")]))

    app_view_fn.__is_component__ = True

    comp = Component(fn=app_view_fn, args=(), kwargs={})

    # First render
    renderer = Renderer(comp)
    renderer.render(app_view_fn)
    assert len(comp._state.hooks) == 2

    # Toggle
    comp._state.hooks[0].value = False
    comp._state.hook_cursor = 0

    # Re-render
    renderer2 = Renderer(comp)
    renderer2.render(app_view_fn)

    # The hook count stays at 2 because use_hook reuses existing hooks
    # by position. This is the mechanism that causes the bug.
    assert len(comp._state.hooks) == 2, (
        "Hook count should remain 2 - the hook at position 1 is reused, "
        "not recreated, which causes stale state"
    )


def test_use_state_preserves_first_initial_value_ignoring_new_initial():
    """
    Reproduces flet-dev/flet#6153.

    Directly demonstrates that use_state ignores the initial value on
    subsequent renders, always returning the value from the first render
    at each hook position. This is correct behavior for same-type state
    but problematic when the branch changes and a completely different
    type of state is expected.
    """
    captured_values = []

    def view_fn():
        _, _ = ft.use_state("toggle_placeholder")
        # On every render, we pass a DIFFERENT initial value,
        # but use_state should return the first one (the stored one).
        val, _ = ft.use_state(lambda: len(captured_values))
        captured_values.append(val)

    view_fn.__is_component__ = True
    comp = Component(fn=view_fn, args=(), kwargs={})

    # First render - initial value is 0 (len([]) == 0)
    renderer = Renderer(comp)
    renderer.render(view_fn)
    assert captured_values[-1] == 0

    # Second render - initial would be 1 (len([0]) == 1), but should return 0
    comp._state.hook_cursor = 0
    renderer2 = Renderer(comp)
    renderer2.render(view_fn)
    assert captured_values[-1] == 0, (
        "use_state should return the stored value (0), not the new initial (1)"
    )

    # Third render - same thing
    comp._state.hook_cursor = 0
    renderer3 = Renderer(comp)
    renderer3.render(view_fn)
    assert captured_values[-1] == 0, (
        "use_state should still return 0, ignoring subsequent initial values"
    )


def test_use_state_stale_observable_type_mismatch_after_toggle():
    """
    Reproduces flet-dev/flet#6153.

    This test demonstrates the type mismatch issue: when toggling
    between branches, use_state returns an instance of the wrong
    observable class. The variable name suggests DifferentApp, but
    the actual value is an App instance.
    """
    results = {}

    def app_view():
        toggle, set_toggle = ft.use_state(True)
        if toggle:
            app, _ = ft.use_state(
                App(users=[User("John", "Doe"), User("Jane", "Doe")])
            )
            results["toggle"] = True
            results["state_type"] = type(app).__name__
            results["user_count"] = len(app.users)
            results["first_user"] = app.users[0].first_name
        else:
            app2, _ = ft.use_state(
                DifferentApp(users=[User("Alice2", "Smith")])
            )
            results["toggle"] = False
            results["state_type"] = type(app2).__name__
            results["user_count"] = len(app2.users)
            results["first_user"] = app2.users[0].first_name

    app_view.__is_component__ = True
    comp = Component(fn=app_view, args=(), kwargs={})

    # First render with toggle=True
    Renderer(comp).render(app_view)
    assert results["toggle"] is True
    assert results["state_type"] == "App"
    assert results["user_count"] == 2
    assert results["first_user"] == "John"

    # Toggle to False
    comp._state.hooks[0].value = False
    comp._state.hook_cursor = 0

    # Re-render with toggle=False
    Renderer(comp).render(app_view)
    assert results["toggle"] is False

    # BUG: The state type should be "DifferentApp" but it's "App"
    assert results["state_type"] == "App", (
        "BUG: state_type is 'App' instead of 'DifferentApp' after toggle"
    )

    # BUG: Should have 1 user (Alice2) but has 2 users (John, Jane)
    assert results["user_count"] == 2, (
        "BUG: user_count is 2 (from App) instead of 1 (from DifferentApp)"
    )

    # BUG: First user should be Alice2 but is John
    assert results["first_user"] == "John", (
        "BUG: first_user is 'John' (from App) instead of 'Alice2' (from DifferentApp)"
    )
