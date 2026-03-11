"""Tests for skipping auto-update when .update() was already called."""

from unittest.mock import AsyncMock, patch

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
    _update_behavior_context_var.set(token.old_value)


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
