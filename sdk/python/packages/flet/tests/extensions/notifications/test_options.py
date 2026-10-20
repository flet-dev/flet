"""Tests for the per-platform options surface."""

import pytest

import flet as ft
from flet_notifications import (
    AndroidForegroundServiceType,
    AndroidOptions,
    AndroidServiceStartType,
    LinuxOptions,
    LocalNotifications,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    ("start_type", "wire_start"),
    [
        (
            AndroidServiceStartType.START_STICKY_COMPATIBILITY,
            "startStickyCompatibility",
        ),
        (AndroidServiceStartType.START_STICKY, "startSticky"),
        (AndroidServiceStartType.START_NOT_STICKY, "startNotSticky"),
        (AndroidServiceStartType.START_REDELIVER_INTENT, "startRedeliverIntent"),
    ],
)
@pytest.mark.asyncio
async def test_fgs_forwards_start_type_and_types(start_type, wire_start):
    """Service enums reach the native boundary as recognized string values."""

    class Recording(LocalNotifications):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def _invoke_method(self, method_name, arguments=None, timeout=None):
            self.calls.append((method_name, encode_wire(arguments)))
            return "ok"

    service = Recording()
    await service.start_foreground_service(
        id=1,
        title="t",
        start_type=start_type,
        foreground_service_types=list(AndroidForegroundServiceType),
    )
    _, args = service.calls[-1]
    assert args["start_type"] == wire_start
    assert args["foreground_service_types"] == [
        "camera",
        "connectedDevice",
        "dataSync",
        "health",
        "location",
        "mediaPlayback",
        "mediaProjection",
        "microphone",
        "phoneCall",
        "remoteMessaging",
        "shortService",
        "specialUse",
        "systemExempted",
    ]


@pytest.mark.parametrize(
    ("timeout", "expected"),
    [
        (ft.Duration(seconds=5), {"seconds": 5}),
        (5000, 5000),
        (0, 0),
        (-1, -1),
        (None, None),
    ],
)
def test_linux_timeout_encodes_duration_and_special_values(timeout, expected):
    """Duration objects and Linux timeout sentinels survive the real transport."""
    assert encode_wire(LinuxOptions(timeout=timeout)).get("timeout") == expected


@pytest.mark.parametrize(
    ("duration", "expected"),
    [(ft.Duration(seconds=2), {"seconds": 2}), (2000, 2000), (0, 0), (None, None)],
)
def test_android_durations_encode_objects_and_milliseconds(duration, expected):
    """Timeout and LED durations use Flet's normal transport representation."""
    wire = encode_wire(
        AndroidOptions(
            timeout_after=duration, led_on_duration=duration, led_off_duration=duration
        )
    )
    for name in ("timeout_after", "led_on_duration", "led_off_duration"):
        assert wire.get(name) == expected
