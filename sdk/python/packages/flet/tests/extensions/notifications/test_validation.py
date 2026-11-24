from unittest.mock import AsyncMock

import pytest

import flet as ft
from flet_notifications import (
    AndroidOptions,
    LinuxOptions,
    NotificationAction,
    NotificationInvalidArgumentException,
    NotificationOptions,
    Notifications,
)


def _service() -> Notifications:
    """A service whose client calls are recorded instead of sent."""
    service = Notifications()
    service._invoke_method = AsyncMock()
    return service


@pytest.mark.asyncio
async def test_invalid_actions_fail_before_the_call():
    """Each action in the list is validated, naming its class."""
    service = _service()
    with pytest.raises(
        NotificationInvalidArgumentException, match="NotificationAction:"
    ):
        await service.show(1, actions=[NotificationAction(id="", title="Open")])
    service._invoke_method.assert_not_called()


@pytest.mark.parametrize(
    ("id", "valid"),
    [(-(2**31) - 1, False), (-(2**31), True), (2**31 - 1, True), (2**31, False)],
)
@pytest.mark.asyncio
async def test_ids_must_fit_32_bits(id, valid):
    """Notification IDs must fit a 32-bit signed integer, bounds included."""
    service = _service()
    if valid:
        await service.show(id)
        service._invoke_method.assert_called_once()
    else:
        with pytest.raises(
            NotificationInvalidArgumentException, match="id must be between"
        ):
            await service.show(id)
        service._invoke_method.assert_not_called()


@pytest.mark.asyncio
async def test_negative_durations_fail_before_the_call():
    """A negative duration nested in the options raises, naming its class."""
    service = _service()
    with pytest.raises(
        NotificationInvalidArgumentException,
        match="AndroidOptions: led_off_duration must not be negative, got -1000 ms",
    ):
        await service.show(
            1,
            options=NotificationOptions(
                android=AndroidOptions(led_off_duration=ft.Duration(seconds=-1))
            ),
        )
    service._invoke_method.assert_not_called()


@pytest.mark.asyncio
async def test_linux_timeout_accepts_the_server_default():
    """`-1`, the notification server's own timeout, is a valid Linux timeout."""
    service = _service()
    await service.show(1, options=NotificationOptions(linux=LinuxOptions(timeout=-1)))
    service._invoke_method.assert_called_once()
