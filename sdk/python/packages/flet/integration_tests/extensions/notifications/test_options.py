"""Tests for the per-platform options surface."""

import json

import msgpack
import pytest

import flet as ft
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet_notifications import (
    AndroidOptions,
    DarwinOptions,
    InterruptionLevel,
    LinuxOptions,
    LinuxUrgency,
    LocalNotifications,
    NotificationOptions,
    Priority,
    Visibility,
    WebOptions,
    WindowsOptions,
    WindowsScenario,
)


@pytest.mark.parametrize(
    ("options_type", "field", "enum_type", "values"),
    [
        (
            AndroidOptions,
            "priority",
            Priority,
            ("min", "low", "default", "high", "max"),
        ),
        (AndroidOptions, "visibility", Visibility, ("public", "private", "secret")),
        (
            DarwinOptions,
            "interruption_level",
            InterruptionLevel,
            ("passive", "active", "timeSensitive", "critical"),
        ),
        (LinuxOptions, "urgency", LinuxUrgency, ("low", "normal", "critical")),
        (
            WindowsOptions,
            "scenario",
            WindowsScenario,
            ("reminder", "alarm", "incomingCall", "urgent"),
        ),
    ],
)
def test_option_enums_preserve_wire_values(options_type, field, enum_type, values):
    """Enum members and legacy strings retain the existing Dart payload."""
    assert tuple(member.value for member in enum_type) == values
    assert options_type().to_dict() == {}
    encoder = configure_encode_object_for_msgpack(ft.Control)

    for value in values:
        for supplied in (enum_type(value), value):
            payload = options_type(**{field: supplied}).to_dict()
            expected = {field: value}
            assert json.loads(json.dumps(payload)) == expected
            assert msgpack.packb(payload, default=encoder) == msgpack.packb(expected)

    # Unknown strings still reach Dart, which applies platform-specific fallbacks.
    assert options_type(**{field: "unknown"}).to_dict() == {field: "unknown"}


def test_options_to_dict_omits_none():
    options = NotificationOptions(
        android=AndroidOptions(silent=True),
        iOS=DarwinOptions(badge_number=3),
    )
    d = options.to_dict()
    assert d["android"] == {"silent": True}
    assert d["iOS"] == {"badge_number": 3}
    assert d["macOS"] is None
    assert d["linux"] is None


def test_android_options_full_round_trip():
    options = AndroidOptions(
        channel_description="Alerts channel",
        channel_bypass_dnd=True,
        icon="ic_stat",
        importance="high",
        priority="max",
        play_sound=False,
        sound="alert_tone",
        enable_vibration=False,
        vibration_pattern=[0, 250, 100],
        channel_show_badge=False,
        auto_cancel=False,
        ongoing=True,
        silent=True,
        color="#FF0000",
        colorized=True,
        large_icon="content://icon",
        only_alert_once=True,
        show_when=False,
        when=1700000000000,
        uses_chronometer=True,
        chronometer_count_down=True,
        sub_text="details",
        number=4,
        visibility="private",
        timeout_after=60000,
        category="alarm",
        full_screen_intent=True,
        shortcut_id="sc",
        additional_flags=["FLAG_INSISTENT"],
        ticker="tick",
        tag="tag1",
        enable_lights=True,
        led_color="#8000FF00",
        led_on_ms=500,
        led_off_ms=500,
    )
    d = options.to_dict()
    assert d["ongoing"] is True
    assert d["color"] == "#FF0000"
    assert d["vibration_pattern"] == [0, 250, 100]
    assert d["category"] == "alarm"
    assert d["led_color"] == "#8000FF00"
    assert len(d) == 35


def test_android_options_hex_validation():
    with pytest.raises(ValueError, match="#RRGGBB"):
        AndroidOptions(color="red")
    with pytest.raises(ValueError, match="#RRGGBB"):
        AndroidOptions(led_color="#FFF")


def test_darwin_options():
    d = DarwinOptions(
        sound="chime",
        badge_number=0,
        subtitle="sub",
        thread_identifier="thread1",
        interruption_level="timeSensitive",
        critical_sound_volume=0.5,
        attachments=["/tmp/a.png"],
        present_banner=False,
    ).to_dict()
    assert d["badge_number"] == 0
    assert d["interruption_level"] == "timeSensitive"
    assert d["attachments"] == ["/tmp/a.png"]
    assert d["present_banner"] is False


def test_linux_windows_web_options():
    assert LinuxOptions(urgency="critical", timeout_ms=5000).to_dict() == {
        "urgency": "critical",
        "timeout_ms": 5000,
    }
    assert WindowsOptions(scenario="alarm", duration="long").to_dict() == {
        "scenario": "alarm",
        "duration": "long",
    }
    assert WebOptions(require_interaction=True, icon_url="x").to_dict() == {
        "require_interaction": True,
        "icon_url": "x",
    }


@pytest.mark.asyncio
async def test_show_forwards_options():
    class Recording(LocalNotifications):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def _invoke_method(self, method_name, arguments=None, timeout=None):
            self.calls.append((method_name, arguments))
            return "ok"

    service = Recording()
    options = NotificationOptions(android=AndroidOptions(ongoing=True))
    await service.show(id=1, title="t", options=options)
    _, args = service.calls[-1]
    assert args["options"] == {
        "android": {"ongoing": True},
        "iOS": None,
        "macOS": None,
        "linux": None,
        "windows": None,
        "web": None,
    }


@pytest.mark.asyncio
async def test_schedule_and_periodic_forward_options():
    from datetime import timedelta

    from flet_notifications import RepeatInterval

    class Recording(LocalNotifications):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def _invoke_method(self, method_name, arguments=None, timeout=None):
            self.calls.append((method_name, arguments))
            return "ok"

    service = Recording()
    options = NotificationOptions(iOS=DarwinOptions(interruption_level="passive"))
    await service.schedule(id=1, when=timedelta(seconds=5), options=options)
    assert service.calls[-1][1]["options"]["iOS"] == {"interruption_level": "passive"}
    await service.periodically_show(
        id=2, repeat_interval=RepeatInterval.HOURLY, options=options
    )
    assert service.calls[-1][1]["options"]["iOS"] == {"interruption_level": "passive"}


@pytest.mark.asyncio
async def test_fgs_forwards_start_type_and_types():
    class Recording(LocalNotifications):
        def __init__(self):
            super().__init__()
            self.calls = []

        async def _invoke_method(self, method_name, arguments=None, timeout=None):
            self.calls.append((method_name, arguments))
            return "ok"

    service = Recording()
    await service.start_foreground_service(
        id=1,
        title="t",
        start_type="startStickyForeground",
        foreground_service_types=["dataSync", "specialUse"],
    )
    _, args = service.calls[-1]
    assert args["start_type"] == "startStickyForeground"
    assert args["foreground_service_types"] == ["dataSync", "specialUse"]
