"""Tests for notification channels."""

import pytest

from flet_notifications import (
    BigTextStyle,
    Importance,
    LocalNotifications,
    NotificationAction,
    NotificationChannel,
    NotificationError,
)

from .helpers import encode_wire


def test_channel_defaults():
    channel = NotificationChannel(id="alerts", name="Alerts")
    d = encode_wire(channel)
    assert d == {"id": "alerts", "name": "Alerts", "description": ""}
    assert channel.importance is Importance.DEFAULT
    assert channel.play_sound is True
    assert channel.enable_vibration is True
    assert channel.show_badge is True
    assert channel.bypass_dnd is False


def test_channel_requires_id_and_name():
    with pytest.raises(ValueError, match="id"):
        NotificationChannel(id="", name="Alerts")
    with pytest.raises(ValueError, match="name"):
        NotificationChannel(id="alerts", name="")


def test_channel_vibration_pattern():
    channel = NotificationChannel(
        id="vib", name="Vibrate", vibration_pattern=[0, 250, 100]
    )
    assert encode_wire(channel)["vibration_pattern"] == [0, 250, 100]


def test_channel_led_color_validated():
    channel = NotificationChannel(
        id="led", name="LED", led_color="#FF0000", enable_lights=True
    )
    assert channel.led_color == "#FF0000"
    with pytest.raises(ValueError, match="hex"):
        NotificationChannel(id="led", name="LED", led_color="red")
    with pytest.raises(ValueError, match="hex"):
        NotificationChannel(id="led", name="LED", led_color="#FFF")


def test_channel_from_dict_round_trip():
    original = NotificationChannel(
        id="c1",
        name="Channel One",
        description="desc",
        importance=Importance.HIGH,
        bypass_dnd=True,
        sound="alert",
    )
    restored = NotificationChannel.from_dict(encode_wire(original))
    assert restored == original


def test_importance_enum_values():
    assert Importance.HIGH.value == "high"
    assert Importance.DEFAULT.value == "defaultImportance"
    assert Importance.MAX.value == "max"


# ── Channel CRUD via the service ───────────────────────────────────────


class _Recording(LocalNotifications):
    def __init__(self):
        super().__init__()
        self.calls: list[tuple[str, dict | None]] = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, encode_wire(arguments)))
        return "ok"


@pytest.mark.asyncio
async def test_create_channel_invokes_wire_payload():
    service = _Recording()
    channel = NotificationChannel(
        id="alerts",
        name="Alerts",
        description="Important",
        importance=Importance.HIGH,
        sound="alert_tone",
        vibration_pattern=[0, 250, 100],
        group_id="updates",
    )
    await service.create_notification_channel(channel)
    name, args = service.calls[-1]
    assert name == "create_notification_channel"
    assert args == {
        "id": "alerts",
        "name": "Alerts",
        "description": "Important",
        "group_id": "updates",
        "importance": "high",
        "sound": "alert_tone",
        "vibration_pattern": [0, 250, 100],
    }


@pytest.mark.asyncio
async def test_delete_channel_invokes_id():
    service = _Recording()
    await service.delete_notification_channel("alerts")
    assert service.calls[-1] == (
        "delete_notification_channel",
        {"channel_id": "alerts"},
    )


@pytest.mark.asyncio
async def test_get_channels_parses_and_error_raises():
    service = _Recording()

    async def invoke(method_name, arguments=None, timeout=None):
        return [{"id": "a", "name": "A", "groupId": "updates", "importance": "low"}]

    service._invoke_method = invoke
    channels = await service.get_notification_channels()
    assert channels[0].group_id == "updates"
    assert channels[0].importance == Importance.LOW

    async def fail(method_name, arguments=None, timeout=None):
        return "error:channel_failed:android only"

    service._invoke_method = fail
    with pytest.raises(NotificationError) as exc:
        await service.get_notification_channels()
    assert exc.value.code == "channel_failed"


@pytest.mark.asyncio
async def test_cancel_with_tag_forwards_tag():
    service = _Recording()
    await service.cancel(5, tag="group")
    assert service.calls[-1] == (
        "cancel",
        {"id": 5, "tag": "group"},
    )
    await service.cancel(5)
    assert service.calls[-1] == ("cancel", {"id": 5})


@pytest.mark.asyncio
async def test_foreground_service_start_stop_and_guard():
    service = _Recording()
    await service.start_foreground_service(
        id=1,
        title="Syncing",
        body="…",
        actions=[NotificationAction(id="done", title="Done")],
        style=BigTextStyle(big_text="long"),
        show_progress=True,
        max_progress=50,
        progress=10,
        channel_id="c",
    )
    name, args = service.calls[-1]
    assert name == "start_foreground_service"
    assert args["actions"] == [
        {
            "id": "done",
            "title": "Done",
        }
    ]
    assert args["style"]["_type"] == "big_text"
    assert args["show_progress"] is True
    assert args["max_progress"] == 50
    assert args["channel_id"] == "c"

    await service.stop_foreground_service()
    assert service.calls[-1] == ("stop_foreground_service", None)

    with pytest.raises(ValueError, match="non-zero"):
        await service.start_foreground_service(id=0)


@pytest.mark.asyncio
async def test_full_screen_intent_permission():
    service = _Recording()

    async def invoke(method_name, arguments=None, timeout=None):
        service.calls.append((method_name, timeout))
        return "true"

    service._invoke_method = invoke
    assert await service.request_full_screen_intent_permission() is True
    assert service.calls[-1] == ("request_full_screen_intent", 300)


def test_all_error_codes_declared():
    from flet_notifications.base import NotificationErrorCode as C

    codes = {
        "unsupported_platform",
        "init_failed",
        "show_failed",
        "schedule_failed",
        "invalid_action",
        "invalid_schedule",
        "invalid_style",
        "invalid_channel",
        "invalid_service_id",
        "invalid_option",
        "channel_failed",
        "foreground_service_failed",
        "query_failed",
        "permission_failed",
        "unknown_method",
    }
    assert {
        C.UNSUPPORTED_PLATFORM,
        C.INIT_FAILED,
        C.SHOW_FAILED,
        C.SCHEDULE_FAILED,
        C.INVALID_ACTION,
        C.INVALID_SCHEDULE,
        C.INVALID_STYLE,
        C.INVALID_CHANNEL,
        C.INVALID_SERVICE_ID,
        C.INVALID_OPTION,
        C.CHANNEL_FAILED,
        C.FOREGROUND_SERVICE_FAILED,
        C.QUERY_FAILED,
        C.PERMISSION_FAILED,
        C.UNKNOWN_METHOD,
    } == codes


def test_hex_color_eight_digit():
    channel = NotificationChannel(
        id="led", name="LED", led_color="#80FF0000", enable_lights=True
    )
    assert channel.led_color == "#80FF0000"


def test_channel_from_dict_unknown_importance_rejected():
    with pytest.raises(ValueError):
        NotificationChannel.from_dict({"id": "x", "name": "X", "importance": "bogus"})
