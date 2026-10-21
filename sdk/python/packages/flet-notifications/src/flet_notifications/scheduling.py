from datetime import datetime, timedelta

import flet as ft
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
    time_zone: str | None,
) -> dict:
    """
    Build the timing fields for a `schedule` invocation.

    Naive datetimes are wall-clock times interpreted in `time_zone` (or the device
    timezone when `time_zone` is None); aware datetimes carry their offset so the exact
    instant is preserved.
    """
    if isinstance(when, timedelta):
        when_payload: dict = {
            "delay_seconds": when.total_seconds(),
            "time_zone": time_zone,
        }
    else:
        when_payload = {
            "iso": when.isoformat(),
            "utc_offset_seconds": when.utcoffset().total_seconds()
            if when.utcoffset() is not None
            else None,
            "time_zone": time_zone,
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
        raise ValueError(
            "repeat_interval must be a RepeatInterval, Duration, or integer"
        )
    if milliseconds is not None and milliseconds < 60000:
        raise ValueError("repeat_interval must be at least one minute")
    return {
        "repeat_interval": repeat_interval,
        "schedule_mode": schedule_mode,
    }
