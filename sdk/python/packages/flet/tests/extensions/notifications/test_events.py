"""Tests for NotificationEvent hydration from Dart payloads."""

import weakref
from unittest.mock import AsyncMock, Mock

import pytest

import flet as ft
from flet.controls.context import _context_page
from flet_notifications import LocalNotifications, NotificationEvent, ResponseType

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
    for field_name in ("on_tap", "on_action", "on_dismiss"):
        resolved = get_event_field_type(service, field_name)
        assert resolved is not None, field_name
        assert resolved != ControlEvent, field_name
        base = getattr(resolved, "__origin__", resolved)
        assert base is NotificationEvent, (
            f"{field_name} resolved to {resolved!r}, expected "
            "ft.EventHandler[NotificationEvent[...]]"
        )


@pytest.mark.parametrize(
    ("wire_type", "event_name", "expected"),
    [
        ("tap", "tap", ResponseType.TAP),
        ("action", "action", ResponseType.ACTION),
        ("dismissed", "dismiss", ResponseType.DISMISSED),
        (None, "tap", ResponseType.TAP),
    ],
)
@pytest.mark.asyncio
async def test_live_event_dispatch_hydrates_response_enum(
    wire_type, event_name, expected
):
    """Real event dispatch supplies enums while retaining Windows reply data."""
    events = []
    service = LocalNotifications(**{f"on_{event_name}": lambda e: events.append(e)})
    session = Mock(index={service._i: service}, after_event=AsyncMock())
    page = ft.Page(sess=session)
    service._parent = weakref.ref(page)
    payload = {
        "id": 1,
        "action_id": "reply" if wire_type == "action" else "",
        "payload": "conversation:1",
        "input": "",
        "data": {"textBox": "typed on windows"} if wire_type == "action" else {},
    }
    if wire_type is not None:
        payload["response_type"] = wire_type
    token = _context_page.set(page)
    try:
        await service._trigger_event(event_name, payload)
    finally:
        _context_page.reset(token)
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, NotificationEvent)
    assert event.response_type is expected
    assert event.control is service
    assert event.name == event_name
    assert event.payload == "conversation:1"
    assert event.data == payload["data"]
    session.after_event.assert_awaited_once_with(service)
