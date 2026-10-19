"""Tests for the LocalNotifications service."""

from datetime import timedelta

import pytest

from flet_notifications import (
    AndroidIcon,
    AndroidOptions,
    BigPictureStyle,
    LocalNotifications,
    NotificationAction,
    NotificationError,
    NotificationOptions,
    RepeatInterval,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    "method_name", ["show", "schedule", "periodically_show", "start_foreground_service"]
)
@pytest.mark.asyncio
async def test_methods_encode_nested_notification_values(method_name):
    service = LocalNotifications()
    calls = []

    async def invoke(name, arguments=None, timeout=None):
        calls.append(arguments)
        return "ok"

    service._invoke_method = invoke
    options = NotificationOptions(android=AndroidOptions(silent=True))
    style = BigPictureStyle(image=AndroidIcon(file_path="/tmp/photo.png"))
    actions = [NotificationAction(id="open", title="Open")]
    kwargs = dict(id=1, options=options, style=style, actions=actions)
    if method_name == "schedule":
        kwargs["when"] = timedelta(seconds=30)
    elif method_name == "periodically_show":
        kwargs["repeat_interval"] = RepeatInterval.HOURLY
    await getattr(service, method_name)(**kwargs)

    args = calls[-1]
    wire = encode_wire(args)
    assert wire["options"] == {"android": {"silent": True}}
    assert wire["style"] == {
        "_type": "big_picture",
        "image": {"file_path": "/tmp/photo.png"},
    }
    assert wire["actions"] == [{"id": "open", "title": "Open"}]


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
