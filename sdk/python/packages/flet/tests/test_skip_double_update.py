"""Tests for skipping auto-update when .update() was already called."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from flet.controls.context import UpdateBehavior, _update_behavior_context_var, context
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


@pytest.fixture(autouse=True)
def _fresh_update_behavior():
    """Ensure each test starts with a clean UpdateBehavior."""
    token = _update_behavior_context_var.set(UpdateBehavior())
    yield
    _update_behavior_context_var.reset(token)


def _make_session():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    return Session(conn)


# --- Context flag unit tests ---


def test_update_called_flag_defaults_to_false():
    assert context.was_update_called() is False


def test_mark_update_called_sets_flag():
    context.mark_update_called()
    assert context.was_update_called() is True


def test_reset_update_called_clears_flag():
    context.mark_update_called()
    context.reset_update_called()
    assert context.was_update_called() is False


def test_reset_auto_update_starts_with_clean_flag():
    context.mark_update_called()
    context.reset_auto_update()
    assert context.was_update_called() is False


# --- after_event integration tests ---


@pytest.mark.asyncio
async def test_after_event_skips_auto_update_when_update_was_called():
    session = _make_session()
    context.mark_update_called()

    with patch.object(
        session, "_Session__auto_update", new_callable=AsyncMock
    ) as mock_auto:
        await session.after_event(session.page)
        mock_auto.assert_not_called()


@pytest.mark.asyncio
async def test_after_event_runs_auto_update_when_update_was_not_called():
    session = _make_session()

    with patch.object(
        session, "_Session__auto_update", new_callable=AsyncMock
    ) as mock_auto:
        await session.after_event(session.page)
        mock_auto.assert_called_once_with(session.page)


@pytest.mark.asyncio
async def test_after_event_resets_flag_after_check():
    session = _make_session()
    context.mark_update_called()

    with patch.object(session, "_Session__auto_update", new_callable=AsyncMock):
        await session.after_event(session.page)

    assert context.was_update_called() is False


@pytest.mark.asyncio
async def test_after_event_resets_flag_even_when_auto_update_disabled():
    session = _make_session()
    context.mark_update_called()
    context.disable_auto_update()

    with patch.object(session, "_Session__auto_update", new_callable=AsyncMock):
        await session.after_event(session.page)

    assert context.was_update_called() is False


# --- Generator handler simulation ---


@pytest.mark.asyncio
async def test_generator_handler_flag_resets_between_yields():
    """Simulate a generator handler where after_event is called after each yield.

    First yield: .update() was called -> skip auto-update
    Second yield: no .update() called  -> auto-update fires
    """
    session = _make_session()

    with patch.object(
        session, "_Session__auto_update", new_callable=AsyncMock
    ) as mock_auto:
        # First yield segment: user called .update()
        context.mark_update_called()
        await session.after_event(session.page)
        assert mock_auto.call_count == 0

        # Second yield segment: no .update() called
        await session.after_event(session.page)
        assert mock_auto.call_count == 1


# --- Page.update() marks the flag ---


def test_page_update_marks_flag():
    session = _make_session()
    page = session.page

    # Page.update() internally calls patch_control which needs a real connection,
    # so we mock __update to isolate the flag-setting behavior.
    with patch.object(page, "_Page__update"):
        page.update()

    assert context.was_update_called() is True


# --- Service (un)registration does not flip the user's update-called flag ---
#
# Services like FilePicker register themselves via an internal `self.update()`
# during `__post_init__`. Before this fix, that flipped the update-called flag,
# which made auto-update think the user had manually called `.update()` and
# suppressed the post-handler auto-update.


def _fake_service():
    svc = MagicMock()
    svc._c = "FakeService"
    svc._i = 999
    return svc


def test_register_service_preserves_unset_flag():
    session = _make_session()
    registry = session.page._services

    with patch.object(registry, "update"):
        assert context.was_update_called() is False
        registry.register_service(_fake_service())
        assert context.was_update_called() is False


def test_register_service_preserves_set_flag():
    session = _make_session()
    registry = session.page._services

    with patch.object(registry, "update"):
        context.mark_update_called()
        registry.register_service(_fake_service())
        assert context.was_update_called() is True


def test_unregister_services_preserves_unset_flag():
    session = _make_session()
    registry = session.page._services
    # Seed with a service whose refcount is low enough to be filtered out.
    registry._services.append(_fake_service())

    with patch.object(registry, "update"):
        assert context.was_update_called() is False
        registry.unregister_services()
        assert context.was_update_called() is False
