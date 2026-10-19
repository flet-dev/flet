"""Tests for the per-platform options surface."""

import pytest

from flet_notifications import (
    AndroidForegroundServiceType,
    AndroidServiceStartType,
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
