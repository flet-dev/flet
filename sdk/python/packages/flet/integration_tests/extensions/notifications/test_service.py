"""Tests for the LocalNotifications service."""

import pytest

import flet_notifications as fn
from flet_notifications import (
    LocalNotifications,
    NotificationAction,
    NotificationActionInput,
    NotificationError,
)


class RecordingService(LocalNotifications):
    """Service whose Dart invokes are recorded instead of sent."""

    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None, int | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, arguments, timeout))
        return "ok"


def test_control_type_string():
    service = LocalNotifications()
    assert service._c == "LocalNotifications"


def test_exports():
    assert fn.__all__ == [
        "ActiveNotification",
        "AndroidIcon",
        "AndroidOptions",
        "AndroidScheduleMode",
        "BigPictureStyle",
        "BigTextStyle",
        "DarwinOptions",
        "DateTimeComponents",
        "GroupAlertBehavior",
        "Importance",
        "InboxStyle",
        "InterruptionLevel",
        "LaunchDetails",
        "LinuxOptions",
        "LinuxUrgency",
        "LocalNotifications",
        "Message",
        "MessagingStyle",
        "NotificationAction",
        "NotificationActionInput",
        "NotificationChannel",
        "NotificationError",
        "NotificationErrorCode",
        "NotificationEvent",
        "NotificationOptions",
        "PendingNotification",
        "Person",
        "Priority",
        "RepeatInterval",
        "ResponseType",
        "Style",
        "Visibility",
        "WebOptions",
        "WindowsOptions",
        "WindowsScenario",
    ]
    assert fn.__version__ == "0.1.4"


def test_before_update_does_not_raise():
    """Notifications are supported on every platform; no guard expected."""
    service = LocalNotifications()
    service.before_update()  # must not raise


@pytest.mark.asyncio
async def test_show_invokes_dart_with_wire_args():
    service = RecordingService()
    action = NotificationAction(
        id="open", title="Open", input=NotificationActionInput(label="Say")
    )
    await service.show(id=7, title="Hi", body="There", payload="x", actions=[action])
    name, args, _ = service.calls[-1]
    assert name == "show"
    assert args == {
        "id": 7,
        "title": "Hi",
        "body": "There",
        "payload": "x",
        "actions": [
            {
                "id": "open",
                "title": "Open",
                "destructive": False,
                "foreground": True,
                "cancel_notification": True,
                "input": {
                    "label": "Say",
                    "choices": [],
                    "allow_free_form_input": True,
                    "allowed_mime_types": [],
                },
            }
        ],
        "style": None,
        "show_progress": False,
        "max_progress": 0,
        "progress": 0,
        "indeterminate": False,
        "group_key": None,
        "set_as_group_summary": False,
        "group_alert_behavior": "all",
        "channel_id": None,
        "options": None,
    }


@pytest.mark.asyncio
async def test_show_without_actions():
    service = RecordingService()
    await service.show(id=1, title="t", body="b")
    name, args, _ = service.calls[-1]
    assert name == "show"
    assert args["actions"] is None
    assert args["payload"] == ""


@pytest.mark.asyncio
async def test_cancel_and_cancel_all():
    service = RecordingService()
    await service.cancel(3)
    assert service.calls[-1] == ("cancel", {"id": 3}, None)
    await service.cancel_all()
    assert service.calls[-1] == ("cancel_all", None, None)


@pytest.mark.asyncio
async def test_request_permissions_uses_long_timeout():
    service = RecordingService()

    async def invoke(method_name, arguments=None, timeout=None):
        service.calls.append((method_name, arguments, timeout))
        return "true"

    service._invoke_method = invoke
    assert await service.request_permissions() is True
    name, _, timeout = service.calls[-1]
    assert name == "request_permissions"
    assert timeout == 300


@pytest.mark.asyncio
async def test_error_result_raises():
    service = LocalNotifications()

    async def fail(method_name, arguments=None, timeout=None):
        return "error:show_failed:boom"

    service._invoke_method = fail
    with pytest.raises(NotificationError) as exc:
        await service.show(id=1, title="t")
    assert exc.value.code == "show_failed"
    assert exc.value.message == "boom"


@pytest.mark.asyncio
async def test_request_permissions_false():
    service = LocalNotifications()

    async def deny(method_name, arguments=None, timeout=None):
        return "false"

    service._invoke_method = deny
    assert await service.request_permissions() is False


def test_service_constructs_outside_page():
    """Services are headless; constructing without a page must not raise
    (registration is simply deferred until a page exists)."""
    service = LocalNotifications()
    assert service._c == "LocalNotifications"
