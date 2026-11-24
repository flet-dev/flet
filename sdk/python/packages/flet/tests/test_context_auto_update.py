import asyncio
import contextvars

import pytest

from flet.controls.context import (
    UpdateBehavior,
    _app_update_behavior,
    _update_behavior_context_var,
    context,
)


@pytest.fixture(autouse=True)
def restore_auto_update_state():
    """Keep these tests from leaking the very state they exercise."""
    previous = _app_update_behavior._auto_update_enabled
    token = _update_behavior_context_var.set(None)
    yield
    _update_behavior_context_var.reset(token)
    _app_update_behavior._auto_update_enabled = previous


def test_context_var_default_is_not_a_shared_mutable_instance():
    """The ContextVar must not default to a shared mutable `UpdateBehavior`.

    Regression test for the defect that made the integration suite
    order-dependent: when the default *was* such an instance, a contextless
    `disable_auto_update()` (e.g. at module import) mutated the very object
    every unrelated context read, turning auto-update off process-wide.

    A brand-new `Context()` is empty, so it exposes the declared default.
    """
    assert contextvars.Context().run(_update_behavior_context_var.get) is None


def test_contextless_call_does_not_mutate_a_shared_context_value():
    assert _update_behavior_context_var.get() is None

    context.disable_auto_update()

    # The setting lands on the explicit app-wide default...
    assert _app_update_behavior._auto_update_enabled is False
    # ...and no context-scoped object was conjured for others to inherit.
    assert _update_behavior_context_var.get() is None


def test_context_scoped_change_does_not_touch_the_app_default():
    context.reset_auto_update()  # what a session/handler does on entry
    assert context.auto_update_enabled() is True

    context.disable_auto_update()

    assert context.auto_update_enabled() is False
    assert _app_update_behavior._auto_update_enabled is True


def test_reset_inherits_enclosing_context():
    context.reset_auto_update()
    context.disable_auto_update()

    context.reset_auto_update()

    assert context.auto_update_enabled() is False


def test_reset_falls_back_to_app_default_without_a_context_value():
    _app_update_behavior._auto_update_enabled = False

    context.reset_auto_update()

    assert context.auto_update_enabled() is False


def test_reset_does_not_inherit_update_called():
    context.reset_auto_update()
    context.mark_update_called()
    assert context.was_update_called() is True

    context.reset_auto_update()

    assert context.was_update_called() is False


@pytest.mark.asyncio
async def test_one_task_cannot_disable_auto_update_for_another():
    """Two concurrent apps in one process must not clobber each other.

    Each event is dispatched in its own task, and a session starts in its own
    task, so both call `reset_auto_update()` on entry and stay isolated.
    """
    observed = {}

    async def app(name: str, disable: bool):
        context.reset_auto_update()
        if disable:
            context.disable_auto_update()
        await asyncio.sleep(0)  # let the other task interleave
        observed[name] = context.auto_update_enabled()

    await asyncio.gather(
        asyncio.create_task(app("disabling", disable=True)),
        asyncio.create_task(app("untouched", disable=False)),
    )

    assert observed == {"disabling": False, "untouched": True}
    assert _app_update_behavior._auto_update_enabled is True


def test_module_scope_disable_is_inherited_by_later_sessions():
    """The documented "disable globally for the app" behaviour still holds."""
    context.disable_auto_update()  # module scope, before any session

    def session():
        context.reset_auto_update()
        return context.auto_update_enabled()

    assert contextvars.copy_context().run(session) is False


def test_update_behavior_defaults():
    behavior = UpdateBehavior()
    assert behavior._auto_update_enabled is True
    assert behavior._update_called is False
