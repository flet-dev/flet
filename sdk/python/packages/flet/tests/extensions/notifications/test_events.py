"""Tests for NotificationEvent hydration from Dart payloads."""

from flet.utils import from_dict
from flet_notifications import LocalNotifications, NotificationEvent

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
        on_tap=lambda e: None, on_action=lambda e: None, on_dismissed=lambda e: None
    )
    for field_name in ("on_tap", "on_action", "on_dismissed"):
        resolved = get_event_field_type(service, field_name)
        assert resolved is not None, field_name
        assert resolved != ControlEvent, field_name
        base = getattr(resolved, "__origin__", resolved)
        assert base is NotificationEvent, (
            f"{field_name} resolved to {resolved!r}, expected "
            "ft.EventHandler[NotificationEvent[...]]"
        )


def test_windows_input_data_reaches_event():
    service = LocalNotifications()
    event = from_dict(
        NotificationEvent,
        {
            "control": service,
            "name": "action",
            "id": 1,
            "action_id": "reply",
            "payload": "",
            "response_type": "action",
            "input": "",
            "data": {"textBox": "typed on windows"},
        },
    )
    # The inherited `data` field carries Windows input values by input id.
    assert event.data == {"textBox": "typed on windows"}
