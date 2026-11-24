"""Tests for the Notifications service."""

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest

import flet as ft
from flet_notifications import (
    AndroidOptions,
    NotificationAction,
    NotificationException,
    NotificationInitializationException,
    NotificationInvalidArgumentException,
    NotificationOptions,
    NotificationPermissionException,
    Notifications,
    NotificationUnsupportedPlatformException,
    RepeatInterval,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    "method_name", ["show", "schedule", "periodically_show", "start_foreground_service"]
)
@pytest.mark.asyncio
async def test_methods_send_the_notification_payload(method_name):
    """Every notification method sends its content, options and actions."""
    service = Notifications()
    service._invoke_method = AsyncMock()
    kwargs = dict(
        id=1,
        title="Title",
        body="Body",
        payload="p",
        options=NotificationOptions(android=AndroidOptions(silent=True)),
        actions=[NotificationAction(id="open", title="Open")],
    )
    if method_name == "schedule":
        kwargs["when"] = timedelta(seconds=30)
    elif method_name == "periodically_show":
        kwargs["repeat_interval"] = RepeatInterval.HOURLY
    await getattr(service, method_name)(**kwargs)

    wire = encode_wire(service._invoke_method.call_args.args[1])
    assert wire["id"] == 1
    assert (wire["title"], wire["body"], wire["payload"]) == ("Title", "Body", "p")
    assert wire["options"] == {"android": {"silent": True}}
    assert wire["actions"] == [{"id": "open", "title": "Open"}]


@pytest.mark.parametrize(
    ("reported", "error", "message"),
    [
        (
            "unsupported_platform: start_foreground_service is not available",
            NotificationUnsupportedPlatformException,
            "start_foreground_service is not available",
        ),
        (
            "initialization_failed: backend unavailable",
            NotificationInitializationException,
            "backend unavailable",
        ),
        (
            "invalid_argument: unknown category",
            NotificationInvalidArgumentException,
            "unknown category",
        ),
        (
            "permission_denied: exact_alarms_not_permitted: denied",
            NotificationPermissionException,
            "exact_alarms_not_permitted: denied",
        ),
        (
            "operation_failed: invalid_icon: missing",
            NotificationException,
            "invalid_icon: missing",
        ),
        (
            "Calling show method of inexistent control: 7",
            NotificationException,
            "Calling show method of inexistent control: 7",
        ),
    ],
)
@pytest.mark.asyncio
async def test_bridge_failures_raise_their_error_class(reported, error, message):
    """A failed call's reported code selects the exception class raised."""
    service = Notifications()

    async def fail(method_name, arguments=None, timeout=None):
        raise RuntimeError(reported)

    service._invoke_method = fail
    with pytest.raises(NotificationException) as exc:
        await service.show(id=1, title="t")
    assert type(exc.value) is error
    assert str(exc.value) == message


@pytest.mark.parametrize(
    ("call", "platform", "web"),
    [
        (lambda n: n.start_foreground_service(1), ft.PagePlatform.IOS, False),
        # A browser session is not the native platform it runs on.
        (lambda n: n.schedule(1, when=timedelta(minutes=1)), ft.PagePlatform.IOS, True),
    ],
)
@pytest.mark.asyncio
async def test_platform_specific_methods_fail_before_the_call(
    client_platform, call, platform, web
):
    """Methods raise on platforms without support, without calling the client."""
    client_platform.platform, client_platform.web = platform, web
    service = Notifications()
    service._invoke_method = AsyncMock()
    with pytest.raises(
        NotificationUnsupportedPlatformException, match="only supported"
    ):
        await call(service)
    service._invoke_method.assert_not_called()


@pytest.mark.asyncio
async def test_web_supported_methods_reach_the_client(client_platform):
    """A method the browser supports is called on the web, whatever its host."""
    client_platform.platform, client_platform.web = ft.PagePlatform.WINDOWS, True
    service = Notifications()
    service._invoke_method = AsyncMock()
    await service.cancel_all_pending()
    service._invoke_method.assert_called_once()
