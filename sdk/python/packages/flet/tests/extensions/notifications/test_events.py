"""Tests for NotificationEvent hydration from Dart payloads."""

import weakref
from unittest.mock import AsyncMock, Mock

import pytest

import flet as ft
from flet.controls.context import _context_page
from flet_notifications import (
    NotificationActionEvent,
    Notifications,
)

# Guards against the ControlEventHandler[X] double-wrap bug: typed payload
# events must resolve to the dataclass, and dispatch must call the handler
# with a hydrated event (not a wrapper).


@pytest.mark.asyncio
async def test_live_event_dispatch_builds_a_typed_event():
    """Real dispatch hands the handler a hydrated action event with its reply."""
    events = []
    service = Notifications(on_action=lambda e: events.append(e))
    session = Mock(index={service._i: service}, after_event=AsyncMock())
    page = ft.Page(sess=session)
    service._parent = weakref.ref(page)
    payload = {
        "id": 1,
        "payload": "conversation:1",
        "action_id": "reply",
        "input": "typed on windows",
        "data": {},
    }
    token = _context_page.set(page)
    try:
        await service._trigger_event("action", payload)
    finally:
        _context_page.reset(token)
    assert len(events) == 1
    event = events[0]
    assert type(event) is NotificationActionEvent
    assert (event.id, event.payload) == (1, "conversation:1")
    assert (event.action_id, event.input) == ("reply", "typed on windows")
