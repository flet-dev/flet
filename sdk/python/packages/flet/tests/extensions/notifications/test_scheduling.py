"""Tests for scheduling APIs."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

import flet as ft
from flet_notifications import Notifications

from .helpers import encode_wire


class RecordingService(Notifications):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return "ok"


@pytest.mark.asyncio
async def test_schedule_naive_datetime_is_device_wall_clock():
    """A naive datetime is sent as wall-clock time, with no timezone of its own."""
    service = RecordingService()
    await service.schedule(id=1, when=datetime(2030, 1, 15, 9, 30))
    _, args = service.calls[-1]
    assert args["when"] == {
        "iso": "2030-01-15T09:30:00",
        "utc_offset_seconds": None,
        "timezone": None,
    }


@pytest.mark.asyncio
async def test_schedule_zoneinfo_datetime_names_its_timezone():
    """A ZoneInfo on `when` keeps its instant and names the zone for recurrence."""
    service = RecordingService()
    when = datetime(2030, 6, 1, 9, 0, tzinfo=ZoneInfo("Europe/Paris"))
    await service.schedule(id=2, when=when)
    _, args = service.calls[-1]
    assert args["when"] == {
        "iso": "2030-06-01T09:00:00+02:00",
        "utc_offset_seconds": 7200,
        "timezone": "Europe/Paris",
    }


@pytest.mark.asyncio
async def test_schedule_timedelta_becomes_an_exact_delay():
    """A timedelta travels as a Flet duration without losing a microsecond."""
    service = RecordingService()
    await service.schedule(id=3, when=timedelta(days=100000, microseconds=1))
    _, args = service.calls[-1]
    assert list(args["when"]) == ["delay"]
    # Flet encodes a Duration as a map of its nonzero units.
    assert (
        ft.Duration.from_unit(**args["when"]["delay"]).in_microseconds
        == 8_640_000_000_000_001
    )
