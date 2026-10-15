"""Tests for NotificationEvent hydration from Dart payloads."""


from flet.utils import from_dict
from flet_notifications import LocalNotifications, NotificationEvent, ResponseType


def _control():
    return LocalNotifications()


def test_event_from_tap_payload():
    control = _control()
    event = from_dict(
        NotificationEvent,
        {
            "control": control,
            "name": "tap",
            "id": 5,
            "action_id": "",
            "payload": "hello",
            "input": "",
            "response_type": "tap",
        },
    )
    assert event.id == 5
    assert event.action_id == ""
    assert event.payload == "hello"
    assert event.input == ""
    assert event.response_type == ResponseType.TAP.value


def test_event_from_action_payload():
    control = _control()
    event = from_dict(
        NotificationEvent,
        {
            "control": control,
            "name": "action",
            "id": 5,
            "action_id": "reply",
            "payload": "hello",
            "input": "my reply text",
            "response_type": "action",
        },
    )
    assert event.action_id == "reply"
    assert event.input == "my reply text"
    assert event.response_type == ResponseType.ACTION.value


def test_event_from_dismissed_payload():
    control = _control()
    event = from_dict(
        NotificationEvent,
        {
            "control": control,
            "name": "dismissed",
            "id": 5,
            "response_type": "dismissed",
        },
    )
    assert event.response_type == ResponseType.DISMISSED.value


def test_event_defaults():
    control = _control()
    event = from_dict(NotificationEvent, {"control": control, "name": "tap"})
    assert event.id == 0
    assert event.action_id == ""
    assert event.payload == ""
    assert event.input == ""
    assert event.response_type == ResponseType.TAP.value


# ── Typed-event resolution regressions ──────────────────────────────────
# Guards against the ControlEventHandler[X] double-wrap bug: typed payload
# events must resolve to the dataclass, and dispatch must call the handler
# with a hydrated event (not a wrapper).


def test_event_field_types_resolve_to_dataclass():
    """Typed payload events must resolve to the dataclass, not Event[...].

    Regression guard: ``from __future__ import annotations`` in the service
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


def test_handlers_use_event_handler_not_control_event_handler():
    """The annotation must be real objects (not PEP 563 strings) of the
    typed-payload form."""
    service = LocalNotifications()
    for field_name in ("on_tap", "on_action", "on_dismissed"):
        handler = getattr(service, field_name)
        assert handler is None
    hints = LocalNotifications.__annotations__
    for field_name in ("on_tap", "on_action", "on_dismissed"):
        annotation = hints[field_name]
        assert not isinstance(annotation, str), (
            f"{field_name} annotation is a string — Flet's event resolver "
            "cannot evaluate it (remove future annotations)"
        )
        # EventHandler[T] expands to Callable[[T], Any]; the payload class
        # must appear directly as the callable's first parameter.
        text = str(annotation)
        assert "NotificationEvent" in text, field_name
        assert "Callable[[flet_notifications.base.NotificationEvent" in text, (
            f"{field_name} is not typed on NotificationEvent: {text}"
        )


def test_handler_assignment_and_hydrated_event():
    service = LocalNotifications()

    async def handler(event):
        pass

    service.on_tap = handler
    assert service.on_tap is handler
    # The handler is invoked by the base control with the event hydrated from
    # the Dart payload; hydrate the same payload directly to verify the
    # mapping the handler receives.
    event = from_dict(
        NotificationEvent,
        {
            "control": service,
            "name": "tap",
            "id": 5,
            "payload": "p",
        },
    )
    assert isinstance(event, NotificationEvent)
    assert event.payload == "p"


def test_windows_input_data_reaches_event():
    from flet.utils import from_dict

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
