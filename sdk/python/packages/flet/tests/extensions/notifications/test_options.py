"""Tests for the per-platform options surface."""

import weakref
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

import flet as ft
from flet_notifications import (
    AndroidForegroundServiceType,
    AndroidOptions,
    AndroidServiceStartType,
    LinuxOptions,
    NotificationAction,
    Notifications,
    NotificationUnsupportedPlatformError,
    WebOptions,
    WindowsOptions,
    WindowsProgress,
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


def test_windows_progress_sends_values_the_client_defaults():
    """Default progress fields are omitted, matching the client's defaults."""
    assert encode_wire(WindowsOptions(progress=WindowsProgress(status="Downloading")))[
        "progress"
    ] == {"status": "Downloading"}
    assert encode_wire(
        WindowsProgress(
            status="Downloading",
            value=3,
            max=10,
            indeterminate=True,
            title="report.pdf",
            label="3/10",
        )
    ) == {
        "status": "Downloading",
        "value": 3,
        "max": 10,
        "indeterminate": True,
        "title": "report.pdf",
        "label": "3/10",
    }


class _RecordingNotifications(Notifications):
    """A service on a page of the given platform, recording its client calls."""

    def __init__(self, platform: ft.PagePlatform, web: bool = False):
        super().__init__()
        self.calls = []
        self._page = ft.Page(sess=Mock())
        self._page.platform = platform
        self._page.web = web
        self._parent = weakref.ref(self._page)

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return False


@pytest.mark.asyncio
async def test_windows_progress_update_sends_the_progress():
    """An in-place update sends the progress and returns the client's answer."""
    service = _RecordingNotifications(ft.PagePlatform.WINDOWS)
    progress = WindowsProgress(status="Downloading...", value=3, max=10, label="3/10")
    assert await service.update_windows_progress(5, progress) is False
    assert service.calls == [
        (
            "update_windows_progress",
            {
                "id": 5,
                "progress": {
                    "status": "Downloading...",
                    "value": 3,
                    "max": 10,
                    "label": "3/10",
                },
            },
        )
    ]


@pytest.mark.parametrize(
    ("platform", "web"),
    [(ft.PagePlatform.ANDROID, False), (ft.PagePlatform.WINDOWS, True)],
)
@pytest.mark.asyncio
async def test_windows_progress_update_is_windows_only(platform, web):
    """Other platforms, and web apps opened on Windows, fail before the call."""
    service = _RecordingNotifications(platform, web)
    with pytest.raises(NotificationUnsupportedPlatformError, match="only available"):
        await service.update_windows_progress(5, WindowsProgress(status="Working"))
    assert service.calls == []


def test_action_sends_require_authentication_only_when_set():
    """The flag reaches the client only when an action requires unlocking."""
    assert "require_authentication" not in encode_wire(
        NotificationAction(id="open", title="Open")
    )
    assert (
        encode_wire(
            NotificationAction(id="delete", title="Delete", require_authentication=True)
        )["require_authentication"]
        is True
    )
