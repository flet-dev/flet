"""Tests for scheduling APIs."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    AndroidScheduleMode,
    DateTimeComponents,
    LocalNotifications,
    NotificationAction,
    PendingNotification,
    RepeatInterval,
)
from flet_notifications.scheduling import (
    build_periodic_args,
    build_schedule_args,
)

from .helpers import encode_wire


class RecordingService(LocalNotifications):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return "ok"


def test_schedule_enum_wire_values():
    assert RepeatInterval.EVERY_MINUTE.value == "everyMinute"
    assert RepeatInterval.HOURLY.value == "hourly"
    assert RepeatInterval.DAILY.value == "daily"
    assert RepeatInterval.WEEKLY.value == "weekly"
    assert DateTimeComponents.TIME.value == "time"
    assert DateTimeComponents.DAY_OF_WEEK_AND_TIME.value == "dayOfWeekAndTime"
    assert DateTimeComponents.DAY_OF_MONTH_AND_TIME.value == "dayOfMonthAndTime"
    assert DateTimeComponents.DATE_AND_TIME.value == "dateAndTime"
    assert AndroidScheduleMode.ALARM_CLOCK.value == "alarmClock"
    assert AndroidScheduleMode.EXACT.value == "exact"
    assert AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE.value == "exactAllowWhileIdle"
    assert AndroidScheduleMode.INEXACT.value == "inexact"
    assert AndroidScheduleMode.INEXACT_ALLOW_WHILE_IDLE.value == (
        "inexactAllowWhileIdle"
    )


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


def test_schedule_signature_has_no_repeat_interval():
    import inspect

    params = inspect.signature(LocalNotifications.schedule).parameters
    assert "repeat_interval" not in params
    assert "match_components" in params
    assert "options" in params


@pytest.mark.asyncio
async def test_schedule_with_actions():
    service = RecordingService()
    await service.schedule(
        id=5,
        when=timedelta(minutes=5),
        actions=[NotificationAction(id="open", title="Open")],
    )
    _, args = service.calls[-1]
    assert args["actions"] == [
        {
            "id": "open",
            "title": "Open",
        }
    ]


@pytest.mark.asyncio
async def test_periodically_show_default():
    service = RecordingService()
    await service.periodically_show(id=6, repeat_interval=RepeatInterval.HOURLY)
    name, args = service.calls[-1]
    assert name == "periodically_show"
    assert args["repeat_interval"] == "hourly"
    assert args["schedule_mode"] == "exactAllowWhileIdle"
    assert args["repeat_duration_seconds"] is None


@pytest.mark.asyncio
async def test_periodically_show_custom_duration():
    service = RecordingService()
    await service.periodically_show(
        id=7,
        repeat_interval=RepeatInterval.DAILY,
        repeat_duration_seconds=900,
    )
    _, args = service.calls[-1]
    assert args["repeat_duration_seconds"] == 900


def test_periodic_builder_rejects_sub_minute_duration():
    with pytest.raises(ValueError, match="at least 60"):
        build_periodic_args(
            id=1,
            repeat_interval=RepeatInterval.DAILY,
            title=None,
            body=None,
            payload="",
            actions=[],
            schedule_mode=AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
            repeat_duration_seconds=30,
        )


@pytest.mark.asyncio
async def test_cancel_pending_and_probes():
    service = RecordingService()
    await service.cancel_pending()
    assert service.calls[-1] == ("cancel_pending", None)

    async def invoke(method_name, arguments=None, timeout=None):
        service.calls.append((method_name, encode_wire(arguments)))
        return "true"

    service._invoke_method = invoke
    assert await service.can_schedule_exact_notifications() is True
    assert await service.request_exact_alarm_permission() is True
    assert service.calls[-1] == ("request_exact_alarm_permission", None)


@pytest.mark.asyncio
async def test_get_pending_parses_records():
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        if method_name == "get_pending":
            return [
                {"id": 1, "title": "A", "body": "b", "payload": "p"},
                {"id": 2, "title": "B", "body": "", "payload": None},
            ]
        return "ok"

    service._invoke_method = invoke
    pending = await service.get_pending_notifications()
    assert pending == [
        PendingNotification(id=1, title="A", body="b", payload="p"),
        PendingNotification(id=2, title="B", body="", payload=""),
    ]


@pytest.mark.asyncio
async def test_get_pending_error_raises():
    from flet_notifications import NotificationError

    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return "error:query_failed:unsupported"

    service._invoke_method = invoke
    with pytest.raises(NotificationError) as exc:
        await service.get_pending_notifications()
    assert exc.value.code == "query_failed"


def test_build_schedule_args_defaults():
    args = build_schedule_args(
        id=1,
        when=timedelta(seconds=5),
        title="t",
        body="b",
        payload="",
        actions=[],
        match_components=None,
        schedule_mode=AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        time_zone=None,
    )
    assert args["actions"] is None
    assert args["match_components"] is None
    assert args["schedule_mode"] is AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE
    assert encode_wire(args)["schedule_mode"] == "exactAllowWhileIdle"
    assert args["options"] is None


# ── Phase 3: rich details forwarding ──────────────────────────────────


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


def test_periodic_forwards_details():
    from flet_notifications import AndroidScheduleMode

    service = RecordingService()
    service.calls.clear()
    import asyncio

    asyncio.run(
        service.periodically_show(
            id=12,
            repeat_interval=RepeatInterval.DAILY,
            schedule_mode=AndroidScheduleMode.INEXACT,
            channel_id="c2",
        )
    )
    _, args = service.calls[-1]
    assert args["schedule_mode"] == "inexact"
    assert args["channel_id"] == "c2"
    assert args["style"] is None
