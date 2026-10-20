"""Tests for the LocalNotifications service."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    AndroidAudioAttributesUsage,
    AndroidIcon,
    AndroidNotificationFlag,
    AndroidOptions,
    BigPictureStyle,
    LocalNotifications,
    NotificationAction,
    NotificationError,
    NotificationOptions,
    RepeatInterval,
    WebNotificationDirection,
    WebOptions,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    "method_name", ["show", "schedule", "periodically_show", "start_foreground_service"]
)
@pytest.mark.parametrize(
    ("flags", "expected_flags"),
    [
        (AndroidNotificationFlag.NONE, 0),
        (0x400, 0x400),
        (AndroidNotificationFlag.INSISTENT | AndroidNotificationFlag.NO_CLEAR, 36),
    ],
)
@pytest.mark.asyncio
async def test_methods_encode_nested_notification_values(
    method_name, flags, expected_flags
):
    service = LocalNotifications()
    calls = []

    async def invoke(name, arguments=None, timeout=None):
        calls.append(arguments)
        return "ok"

    service._invoke_method = invoke
    options = NotificationOptions(
        android=AndroidOptions(
            silent=True,
            show_timestamp=False,
            icon="ic_stat_notify",
            audio_attributes_usage=AndroidAudioAttributesUsage.ALARM,
            additional_flags=flags,
        ),
        web=WebOptions(
            direction=WebNotificationDirection.RIGHT_TO_LEFT,
            icon_url="/assets/icon.png",
            require_interaction=True,
            is_silent=False,
            timestamp=datetime(2023, 11, 14, 22, 13, 20, 123000, tzinfo=timezone.utc),
        ),
    )
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
    assert wire["options"] == {
        "android": {
            "silent": True,
            "show_timestamp": False,
            "icon": "ic_stat_notify",
            "audio_attributes_usage": "alarm",
            "additional_flags": expected_flags,
        },
        "web": {
            "direction": "rightToLeft",
            "icon_url": "/assets/icon.png",
            "require_interaction": True,
            "is_silent": False,
            "timestamp": datetime(
                2023, 11, 14, 22, 13, 20, 123000, tzinfo=timezone.utc
            ),
        },
    }
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
