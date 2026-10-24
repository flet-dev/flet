from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import flet as ft
from flet_notifications.base import NotificationInvalidArgumentError
from flet_notifications.types import (
    AndroidScheduleMode,
    DateTimeComponents,
    RepeatInterval,
)

__all__ = []


def build_schedule_args(
    *,
    when: datetime | timedelta,
    match_components: DateTimeComponents | None,
    schedule_mode: AndroidScheduleMode,
) -> dict:
    """
    Build the timing fields for a `schedule` invocation.

    Naive datetimes are wall-clock times in the device timezone; aware datetimes carry
    their offset so the exact instant is preserved. A `ZoneInfo` on `when` also names
    the timezone used for calendar recurrence.
    """
    timezone = (
        when.tzinfo.key
        if isinstance(when, datetime) and isinstance(when.tzinfo, ZoneInfo)
        else None
    )

    if isinstance(when, timedelta):
        if when <= timedelta(0):
            raise NotificationInvalidArgumentError("when must be in the future")
        when_payload = {
            "delay": ft.Duration.from_unit(
                microseconds=when // timedelta(microseconds=1)
            )
        }
    else:
        when_payload = {
            "iso": when.isoformat(),
            "utc_offset_seconds": when.utcoffset().total_seconds()
            if when.utcoffset() is not None
            else None,
            "timezone": timezone,
        }

    return {
        "when": when_payload,
        "match_components": match_components,
        "schedule_mode": schedule_mode,
    }


def build_periodic_args(
    *,
    repeat_interval: RepeatInterval | ft.DurationValue,
    schedule_mode: AndroidScheduleMode,
) -> dict:
    """Validate the interval and build periodic scheduling fields."""
    if isinstance(repeat_interval, ft.Duration):
        milliseconds = repeat_interval.in_milliseconds
    elif isinstance(repeat_interval, int):
        milliseconds = repeat_interval
    elif isinstance(repeat_interval, RepeatInterval):
        milliseconds = None
    else:
        raise NotificationInvalidArgumentError(
            "repeat_interval must be a RepeatInterval, Duration, or integer"
        )
    if milliseconds is not None and milliseconds < 60000:
        raise NotificationInvalidArgumentError(
            "repeat_interval must be at least one minute"
        )
    return {
        "repeat_interval": repeat_interval,
        "schedule_mode": schedule_mode,
    }
