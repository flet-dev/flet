"""Tests for scheduling APIs."""

from datetime import datetime, timedelta, timezone

import pytest

import flet as ft
from flet_notifications import (
    AndroidGroup,
    AndroidOptions,
    AndroidProgress,
    BigTextStyle,
    DateTimeComponents,
    GroupAlertBehavior,
    LocalNotifications,
    NotificationOptions,
    RepeatInterval,
)

from .helpers import encode_wire


class RecordingService(LocalNotifications):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return "ok"


@pytest.mark.parametrize(
    ("interval", "expected"),
    [
        *((interval, interval.value) for interval in RepeatInterval),
        (ft.Duration(minutes=15), {"minutes": 15}),
        (ft.Duration(seconds=60), {"seconds": 60}),
        (
            ft.Duration(seconds=60, milliseconds=500),
            {"seconds": 60, "milliseconds": 500},
        ),
        (60000, 60000),
    ],
)
@pytest.mark.asyncio
async def test_periodic_interval_encodes_presets_and_custom_durations(
    interval, expected
):
    """Preset and custom intervals share one argument through the real transport."""
    service = RecordingService()
    await service.periodically_show(id=1, repeat_interval=interval)
    name, args = service.calls[-1]
    assert name == "periodically_show"
    assert args["repeat_interval"] == expected
    assert "repeat_duration_seconds" not in args


@pytest.mark.parametrize(
    "interval",
    [
        ft.Duration(seconds=59, milliseconds=999, microseconds=999),
        ft.Duration(),
        ft.Duration(minutes=-1),
        59999,
        0,
        -1,
        "daily",
        None,
    ],
)
@pytest.mark.asyncio
async def test_invalid_periodic_interval_fails_before_invocation(interval):
    """Invalid types and sub-minute intervals never reach the client."""
    service = RecordingService()
    with pytest.raises(ValueError, match="repeat_interval"):
        await service.periodically_show(id=1, repeat_interval=interval)
    assert service.calls == []


@pytest.mark.asyncio
async def test_schedule_naive_datetime_with_timezone():
    service = RecordingService()
    when = datetime(2030, 1, 15, 9, 30)
    await service.schedule(
        id=1,
        when=when,
        title="t",
        body="b",
        time_zone="Africa/Lagos",
        match_components=DateTimeComponents.TIME,
    )
    name, args = service.calls[-1]
    assert name == "schedule"
    assert args["when"] == {
        "iso": "2030-01-15T09:30:00",
        "utc_offset_seconds": None,
        "time_zone": "Africa/Lagos",
    }
    assert args["match_components"] == "time"
    assert args["schedule_mode"] == "exactAllowWhileIdle"
    assert args["options"] is None


@pytest.mark.asyncio
async def test_schedule_aware_datetime_carries_offset():
    service = RecordingService()
    when = datetime(2030, 6, 1, 12, 0, tzinfo=timezone(timedelta(hours=1)))
    await service.schedule(id=2, when=when)
    _, args = service.calls[-1]
    assert args["when"]["iso"] == "2030-06-01T12:00:00+01:00"
    assert args["when"]["utc_offset_seconds"] == 3600
    assert args["when"]["time_zone"] is None


@pytest.mark.parametrize(
    ("delay", "microseconds"),
    [
        (timedelta(seconds=30), 30_000_000),
        (timedelta(seconds=1, microseconds=500001), 1_500_001),
        (timedelta(milliseconds=500), 500_000),
        (timedelta(microseconds=1), 1),
        (timedelta(), 0),
        (timedelta(microseconds=-1), -1),
        (timedelta(days=100000, microseconds=1), 8_640_000_000_000_001),
    ],
)
@pytest.mark.asyncio
async def test_schedule_timedelta_becomes_delay(delay, microseconds):
    """Timedeltas retain exact integer microseconds through the transport."""
    service = RecordingService()
    await service.schedule(id=3, when=delay)
    _, args = service.calls[-1]
    assert args["when"] == {
        "delay_ms": microseconds,
        "time_zone": None,
    }
    assert type(args["when"]["delay_ms"]) is int


@pytest.mark.asyncio
async def test_schedule_forwards_android_style_progress_and_group():
    """Android layout, progress, group and channel travel inside the options."""
    service = RecordingService()
    await service.schedule(
        id=11,
        when=timedelta(seconds=5),
        options=NotificationOptions(
            android=AndroidOptions(
                channel_id="c1",
                style=BigTextStyle(big_text="long"),
                progress=AndroidProgress(value=25),
                group=AndroidGroup(
                    key="grp",
                    summary=True,
                    alert_behavior=GroupAlertBehavior.SUMMARY,
                ),
            )
        ),
    )
    _, args = service.calls[-1]
    assert encode_wire(args["options"]) == {
        "android": {
            "channel_id": "c1",
            "style": {"_type": "big_text", "big_text": "long"},
            "progress": {"value": 25},
            "group": {"key": "grp", "summary": True, "alert_behavior": "summary"},
        }
    }
