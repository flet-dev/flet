"""Schedule argument serialization (pure — unit tested)."""

from datetime import datetime, timedelta

from flet_notifications.styles import Style, prepare_style
from flet_notifications.types import (
    AndroidScheduleMode,
    DateTimeComponents,
    GroupAlertBehavior,
    RepeatInterval,
)


def build_schedule_args(
    *,
    id: int,
    when: datetime | timedelta,
    title: str | None,
    body: str | None,
    payload: str,
    actions: list,
    match_components: DateTimeComponents | None,
    schedule_mode: AndroidScheduleMode,
    time_zone: str | None,
    options: object | None = None,
    style: Style | None = None,
    show_progress: bool = False,
    max_progress: int = 0,
    progress: int = 0,
    indeterminate: bool = False,
    group_key: str | None = None,
    set_as_group_summary: bool = False,
    group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
    channel_id: str | None = None,
) -> dict:
    """Build the `schedule` invoke payload.

    Naive datetimes are wall-clock times interpreted in `time_zone` (or the
    device timezone when `time_zone` is None); aware datetimes carry their
    offset so the exact instant is preserved.
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
        "id": id,
        "title": title,
        "body": body,
        "payload": payload,
        "actions": actions or None,
        "when": when_payload,
        "match_components": match_components,
        "options": options,
        "schedule_mode": schedule_mode,
        "style": prepare_style(style),
        "show_progress": show_progress,
        "max_progress": max_progress,
        "progress": progress,
        "indeterminate": indeterminate,
        "group_key": group_key,
        "set_as_group_summary": set_as_group_summary,
        "group_alert_behavior": group_alert_behavior,
        "channel_id": channel_id,
    }


def build_periodic_args(
    *,
    id: int,
    repeat_interval: RepeatInterval,
    title: str | None,
    body: str | None,
    payload: str,
    actions: list,
    schedule_mode: AndroidScheduleMode,
    repeat_duration_seconds: int | None,
    options: object | None = None,
    style: Style | None = None,
    show_progress: bool = False,
    max_progress: int = 0,
    progress: int = 0,
    indeterminate: bool = False,
    group_key: str | None = None,
    set_as_group_summary: bool = False,
    group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
    channel_id: str | None = None,
) -> dict:
    """Build the `periodically_show` invoke payload."""
    if repeat_duration_seconds is not None and repeat_duration_seconds < 60:
        raise ValueError("repeat_duration_seconds must be at least 60")
    return {
        "id": id,
        "title": title,
        "body": body,
        "payload": payload,
        "actions": actions or None,
        "repeat_interval": repeat_interval,
        "schedule_mode": schedule_mode,
        "repeat_duration_seconds": repeat_duration_seconds,
        "options": options,
        "style": prepare_style(style),
        "show_progress": show_progress,
        "max_progress": max_progress,
        "progress": progress,
        "indeterminate": indeterminate,
        "group_key": group_key,
        "set_as_group_summary": set_as_group_summary,
        "group_alert_behavior": group_alert_behavior,
        "channel_id": channel_id,
    }
