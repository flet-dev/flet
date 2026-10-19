"""Tests for scheduling APIs."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    DateTimeComponents,
    LocalNotifications,
)

from .helpers import encode_wire


class RecordingService(LocalNotifications):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return "ok"


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


@pytest.mark.asyncio
async def test_schedule_timedelta_becomes_delay():
    service = RecordingService()
    await service.schedule(id=3, when=timedelta(seconds=30))
    _, args = service.calls[-1]
    assert args["when"] == {
        "delay_seconds": 30.0,
        "time_zone": None,
    }


def test_schedule_forwards_style_progress_grouping():
    from flet_notifications import BigTextStyle, GroupAlertBehavior

    service = RecordingService()
    service.calls.clear()
    # recorded via the synchronous RecordingService path
    import asyncio

    asyncio.run(
        service.schedule(
            id=11,
            when=timedelta(seconds=5),
            style=BigTextStyle(big_text="long"),
            show_progress=True,
            max_progress=100,
            progress=25,
            group_key="grp",
            set_as_group_summary=True,
            group_alert_behavior=GroupAlertBehavior.SUMMARY,
            channel_id="c1",
        )
    )
    _, args = service.calls[-1]
    assert args["style"] == {
        "_type": "big_text",
        "big_text": "long",
    }
    assert args["show_progress"] is True
    assert args["max_progress"] == 100
    assert args["progress"] == 25
    assert args["group_key"] == "grp"
    assert args["set_as_group_summary"] is True
    assert args["group_alert_behavior"] == "summary"
    assert args["channel_id"] == "c1"
