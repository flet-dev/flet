"""Tests for the per-platform options surface."""

from datetime import datetime, timedelta, timezone

import pytest

import flet as ft
from flet_notifications import (
    AndroidForegroundServiceType,
    AndroidOptions,
    AndroidServiceStartType,
    LinuxOptions,
    Notifications,
    WebOptions,
    WindowsOptions,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    "timestamp",
    [
        datetime(2030, 6, 1, 12, 0, 0, 123000, tzinfo=timezone.utc),
        datetime(2030, 6, 1, 14, 0, 0, 123000, tzinfo=timezone(timedelta(hours=2))),
        datetime(2030, 6, 1, 7, 0, 0, 123000, tzinfo=timezone(timedelta(hours=-5))),
        datetime(2030, 6, 1, 0, 30, tzinfo=timezone(timedelta(hours=2))),
        datetime(2030, 6, 1, 23, 30, tzinfo=timezone(timedelta(hours=-5))),
        datetime(2030, 6, 1, 12, 0, 0, 123000),
        None,
    ],
)
def test_display_timestamps_preserve_instants_through_transport(timestamp):
    """Display timestamps use UTC transport, preserving aware and naive instants."""
    expected = timestamp.astimezone(timezone.utc) if timestamp is not None else None
    for options, field in (
        (AndroidOptions(timestamp=timestamp), "timestamp"),
        (WindowsOptions(timestamp=timestamp), "timestamp"),
        (WebOptions(timestamp=timestamp), "timestamp"),
    ):
        actual = encode_wire(options).get(field)
        assert actual == expected
        if actual is not None:
            assert actual.utcoffset() == timedelta(0)


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

    class Recording(Notifications):
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
