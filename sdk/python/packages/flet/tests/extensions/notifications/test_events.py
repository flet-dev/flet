"""Tests for NotificationEvent hydration from Dart payloads."""

import weakref
from unittest.mock import AsyncMock, Mock

import pytest

import flet as ft
from flet.controls.context import _context_page
from flet_notifications import (
    LocalNotifications,
    NotificationActionEvent,
    NotificationEvent,
)

# Guards against the ControlEventHandler[X] double-wrap bug: typed payload
# events must resolve to the dataclass, and dispatch must call the handler
# with a hydrated event (not a wrapper).


def test_event_field_types_resolve_to_dataclass():
    """Typed payload events must resolve to the dataclass, not Event[...].

    Regression guard: `from __future__ import annotations` in the service
    module makes flet's resolver raise, silently breaking dispatch.
    """
    from flet.controls.control_event import ControlEvent, get_event_field_type

    service = LocalNotifications(
        on_tap=lambda e: None, on_action=lambda e: None, on_dismiss=lambda e: None
    )
    for field_name, expected in (
        ("on_tap", NotificationEvent),
        ("on_action", NotificationActionEvent),
        ("on_dismiss", NotificationEvent),
    ):
        resolved = get_event_field_type(service, field_name)
        assert resolved is not None, field_name
        assert resolved != ControlEvent, field_name
        base = getattr(resolved, "__origin__", resolved)
        assert base is expected, (
            f"{field_name} resolved to {resolved!r}, expected "
            f"ft.EventHandler[{expected.__name__}[...]]"
        )


@pytest.mark.parametrize("event_name", ["tap", "action", "dismiss"])
@pytest.mark.asyncio
async def test_live_event_dispatch_builds_each_handlers_event(event_name):
    """Real dispatch builds an action event only for actions, keeping reply data."""
    events = []
    service = LocalNotifications(**{f"on_{event_name}": lambda e: events.append(e)})
    session = Mock(index={service._i: service}, after_event=AsyncMock())
    page = ft.Page(sess=session)
    service._parent = weakref.ref(page)
    payload = {"id": 1, "payload": "conversation:1", "data": {}}
    if event_name == "action":
        payload.update(
            action_id="reply",
            input="typed on windows",
            data={"textBox": "typed on windows"},
        )
    token = _context_page.set(page)
    try:
        await service._trigger_event(event_name, payload)
    finally:
        _context_page.reset(token)
    assert len(events) == 1
    event = events[0]
    assert type(event) is (
        NotificationActionEvent if event_name == "action" else NotificationEvent
    )
    assert event.control is service
    assert event.name == event_name
    assert event.id == 1
    assert event.payload == "conversation:1"
    assert event.data == payload["data"]
    if event_name == "action":
        assert event.action_id == "reply"
        assert event.input == "typed on windows"
    session.after_event.assert_awaited_once_with(service)
