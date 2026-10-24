from unittest.mock import AsyncMock

import pytest

import flet as ft
from flet_notifications import (
    AndroidGroup,
    AndroidInboxStyle,
    AndroidOptions,
    AndroidProgress,
    DarwinOptions,
    LinuxOptions,
    NotificationAction,
    NotificationChannel,
    NotificationInvalidArgumentError,
    NotificationOptions,
    Notifications,
    WindowsOptions,
    WindowsProgress,
)


def _service() -> Notifications:
    """A service whose client calls are recorded instead of sent."""
    service = Notifications()
    service._invoke_method = AsyncMock()
    return service


@pytest.mark.parametrize(
    ("options", "message"),
    [
        (
            NotificationOptions(
                android=AndroidOptions(progress=AndroidProgress(value=-1))
            ),
            "AndroidProgress: value must be greater than or equal to 0",
        ),
        (
            NotificationOptions(
                android=AndroidOptions(progress=AndroidProgress(value=150))
            ),
            r"AndroidProgress: value \(150\) must be less than or equal to max",
        ),
        (
            NotificationOptions(
                android=AndroidOptions(progress=AndroidProgress(max=0))
            ),
            "AndroidProgress: max must be strictly greater than 0",
        ),
        (
            NotificationOptions(android=AndroidOptions(group=AndroidGroup(key=""))),
            "AndroidGroup: key must be non-empty",
        ),
        (
            NotificationOptions(android=AndroidOptions(number=-1)),
            "AndroidOptions: number must be greater than or equal to 0",
        ),
        (
            NotificationOptions(
                android=AndroidOptions(channel=NotificationChannel(id="", name="C"))
            ),
            "NotificationChannel: id must be non-empty",
        ),
        (
            NotificationOptions(
                android=AndroidOptions(style=AndroidInboxStyle(lines=[]))
            ),
            "AndroidInboxStyle: lines must be non-empty",
        ),
        (
            NotificationOptions(ios=DarwinOptions(badge_number=-1)),
            "DarwinOptions: badge_number must be greater than or equal to 0",
        ),
        (
            NotificationOptions(macos=DarwinOptions(critical_sound_volume=1.5)),
            "DarwinOptions: critical_sound_volume must be between 0.0 and 1.0",
        ),
        (
            NotificationOptions(
                windows=WindowsOptions(progress=WindowsProgress(status=""))
            ),
            "WindowsProgress: status must be non-empty",
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_options_fail_before_the_call(options, message):
    """Nested option values that break a rule raise, naming their class."""
    service = _service()
    with pytest.raises(NotificationInvalidArgumentError, match=message):
        await service.show(1, options=options)
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize(
    ("action", "message"),
    [
        (NotificationAction(id="", title="Open"), "NotificationAction: id"),
        (NotificationAction(id="open", title=""), "NotificationAction: title"),
    ],
)
@pytest.mark.asyncio
async def test_invalid_actions_fail_before_the_call(action, message):
    """Actions need an ID and a title."""
    service = _service()
    with pytest.raises(NotificationInvalidArgumentError, match=message):
        await service.show(1, actions=[action])
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize("id", [-(2**31) - 1, 2**31])
@pytest.mark.parametrize(
    "call",
    [
        lambda n, id: n.show(id),
        lambda n, id: n.cancel(id),
        lambda n, id: n.start_foreground_service(id),
    ],
)
@pytest.mark.asyncio
async def test_ids_outside_32_bits_fail_before_the_call(call, id):
    """Notification IDs must fit a 32-bit signed integer."""
    service = _service()
    with pytest.raises(NotificationInvalidArgumentError, match="id must be between"):
        await call(service, id)
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize("id", [-(2**31), 0, 2**31 - 1])
@pytest.mark.asyncio
async def test_ids_within_32_bits_reach_the_client(id):
    """The full 32-bit signed range is accepted."""
    service = _service()
    await service.cancel(id)
    service._invoke_method.assert_called_once()


@pytest.mark.asyncio
async def test_valid_nested_values_reach_the_client():
    """Values within their rules pass, however deeply nested."""
    service = _service()
    await service.show(
        1,
        actions=[NotificationAction(id="open", title="Open")],
        options=NotificationOptions(
            android=AndroidOptions(
                progress=AndroidProgress(value=100),
                channel=NotificationChannel(id="downloads", name="Downloads"),
                number=0,
            ),
            ios=DarwinOptions(badge_number=0, critical_sound_volume=1.0),
        ),
    )
    service._invoke_method.assert_called_once()


@pytest.mark.asyncio
async def test_channels_are_validated_when_created():
    """A channel created on its own is checked too."""
    service = _service()
    with pytest.raises(
        NotificationInvalidArgumentError, match="name must be non-empty"
    ):
        await service.create_notification_channel(NotificationChannel(id="c", name=""))
    service._invoke_method.assert_not_called()


@pytest.mark.asyncio
async def test_windows_progress_updates_are_validated(client_platform):
    """An in-place progress update is checked before the call."""
    client_platform.platform = ft.PagePlatform.WINDOWS
    service = _service()
    with pytest.raises(NotificationInvalidArgumentError, match="WindowsProgress"):
        await service.update_windows_progress(
            1, WindowsProgress(status="Downloading", value=5, max=4)
        )
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize(
    ("options", "message"),
    [
        (
            NotificationOptions(android=AndroidOptions(timeout_after=-1)),
            "AndroidOptions: timeout_after must not be negative, got -1 ms",
        ),
        (
            NotificationOptions(
                android=AndroidOptions(led_off_duration=ft.Duration(seconds=-1))
            ),
            "AndroidOptions: led_off_duration must not be negative, got -1000 ms",
        ),
        (
            NotificationOptions(linux=LinuxOptions(timeout=-2)),
            "LinuxOptions: timeout must not be negative, except -1, got -2 ms",
        ),
    ],
)
@pytest.mark.asyncio
async def test_negative_durations_fail_before_the_call(options, message):
    """Durations can't be negative, apart from documented special values."""
    service = _service()
    with pytest.raises(NotificationInvalidArgumentError, match=message):
        await service.show(1, options=options)
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize("timeout", [-1, 0, ft.Duration(seconds=5)])
@pytest.mark.asyncio
async def test_linux_timeout_special_values_reach_the_client(timeout):
    """`-1` (the server's timeout) and `0` (no expiry) are valid Linux timeouts."""
    service = _service()
    await service.show(
        1, options=NotificationOptions(linux=LinuxOptions(timeout=timeout))
    )
    service._invoke_method.assert_called_once()


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda n: n.delete_notification_channel(""), "channel_id"),
        (
            lambda n: n.create_notification_channel_group("", name="Group"),
            "group_id",
        ),
        (lambda n: n.create_notification_channel_group("g", name=""), "name"),
        (lambda n: n.delete_notification_channel_group(""), "group_id"),
    ],
)
@pytest.mark.asyncio
async def test_empty_channel_and_group_ids_fail_before_the_call(call, message):
    """Channel and group methods need non-empty IDs and names."""
    service = _service()
    with pytest.raises(
        NotificationInvalidArgumentError, match=f"{message} must be non-empty"
    ):
        await call(service)
    service._invoke_method.assert_not_called()
