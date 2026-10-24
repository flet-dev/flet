"""Tests for the Notifications service."""

from datetime import datetime, timedelta, timezone

import pytest

import flet as ft
from flet_notifications import (
    AndroidAudioAttributesUsage,
    AndroidBigPictureStyle,
    AndroidFileBitmap,
    AndroidNotificationFlag,
    AndroidOptions,
    NotificationAction,
    NotificationChannel,
    NotificationError,
    NotificationInitializationError,
    NotificationInvalidArgumentError,
    NotificationOptions,
    NotificationPermissionError,
    Notifications,
    NotificationUnsupportedPlatformError,
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
    service = Notifications()
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
            channel=NotificationChannel(
                id="alarms",
                name="Alarms",
                audio_attributes_usage=AndroidAudioAttributesUsage.ALARM,
            ),
            additional_flags=flags,
            style=AndroidBigPictureStyle(
                image=AndroidFileBitmap(path="/tmp/photo.png")
            ),
        ),
        web=WebOptions(
            direction=WebNotificationDirection.RIGHT_TO_LEFT,
            icon_url="/assets/icon.png",
            require_interaction=True,
            is_silent=False,
            timestamp=datetime(2023, 11, 14, 22, 13, 20, 123000, tzinfo=timezone.utc),
        ),
    )
    actions = [NotificationAction(id="open", title="Open")]
    kwargs = dict(id=1, options=options, actions=actions)
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
            "channel": {
                "id": "alarms",
                "name": "Alarms",
                "audio_attributes_usage": "alarm",
            },
            "additional_flags": expected_flags,
            "style": {
                "_type": "big_picture",
                "image": {"_type": "file", "path": "/tmp/photo.png"},
            },
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
    assert wire["actions"] == [{"id": "open", "title": "Open"}]


@pytest.mark.parametrize(
    ("reported", "error", "message"),
    [
        (
            "unsupported_platform: start_foreground_service is not available",
            NotificationUnsupportedPlatformError,
            "start_foreground_service is not available",
        ),
        (
            "initialization_failed: backend unavailable",
            NotificationInitializationError,
            "backend unavailable",
        ),
        (
            "invalid_argument: unknown category",
            NotificationInvalidArgumentError,
            "unknown category",
        ),
        (
            "permission_denied: exact_alarms_not_permitted: denied",
            NotificationPermissionError,
            "exact_alarms_not_permitted: denied",
        ),
        (
            "operation_failed: invalid_icon: missing",
            NotificationError,
            "invalid_icon: missing",
        ),
        (
            "Calling show method of inexistent control: 7",
            NotificationError,
            "Calling show method of inexistent control: 7",
        ),
    ],
)
@pytest.mark.asyncio
async def test_bridge_failures_raise_their_error_class(reported, error, message):
    """A failed call's reported code selects the NotificationError subclass raised."""
    service = Notifications()

    async def fail(method_name, arguments=None, timeout=None):
        raise RuntimeError(reported)

    service._invoke_method = fail
    with pytest.raises(NotificationError) as exc:
        await service.show(id=1, title="t")
    assert type(exc.value) is error
    assert str(exc.value) == message


def test_error_classes_are_also_caught_as_their_generic_kinds():
    """Unsupported-platform and invalid-argument errors match Flet and Python bases."""
    assert issubclass(
        NotificationUnsupportedPlatformError, ft.FletUnsupportedPlatformException
    )
    assert issubclass(NotificationInvalidArgumentError, ValueError)


@pytest.mark.parametrize(
    ("method", "native_method", "timeout"),
    [
        ("request_permissions", "request_permissions", 300),
        ("can_schedule_exact_notifications", "can_schedule_exact_notifications", None),
        ("request_exact_alarm_permission", "request_exact_alarm_permission", 300),
        ("are_notifications_enabled", "are_notifications_enabled", None),
        ("request_full_screen_intent_permission", "request_full_screen_intent", 300),
        ("has_notification_policy_access", "has_notification_policy_access", None),
        (
            "request_notification_policy_access",
            "request_notification_policy_access",
            300,
        ),
    ],
)
@pytest.mark.asyncio
async def test_boolean_methods_preserve_native_results_and_errors(
    method, native_method, timeout
):
    """Boolean results survive transport without hiding errors or changing timeouts."""
    service = Notifications()
    result = False

    async def invoke(method_name, arguments=None, timeout=None):
        assert method_name == native_method
        assert timeout == expected_timeout
        if isinstance(result, Exception):
            raise result
        return encode_wire(result)

    expected_timeout = timeout
    service._invoke_method = invoke
    for result in [True, False]:
        assert await getattr(service, method)() is result
    result = RuntimeError("initialization_failed: backend unavailable")
    with pytest.raises(NotificationError) as exc:
        await getattr(service, method)()
    assert type(exc.value) is NotificationInitializationError
    assert str(exc.value) == "backend unavailable"


@pytest.mark.asyncio
async def test_request_permissions_sends_the_requested_apple_authorizations():
    """Apple authorization kinds travel as arguments, defaulting to a full prompt."""
    service = Notifications()
    calls = []

    async def invoke(method_name, arguments=None, timeout=None):
        calls.append(arguments)
        return True

    service._invoke_method = invoke
    await service.request_permissions()
    await service.request_permissions(alert=False, critical=True, provisional=True)
    assert calls == [
        {
            "alert": True,
            "sound": True,
            "badge": True,
            "critical": False,
            "provisional": False,
        },
        {
            "alert": False,
            "sound": True,
            "badge": True,
            "critical": True,
            "provisional": True,
        },
    ]
