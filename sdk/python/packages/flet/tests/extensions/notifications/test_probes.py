"""Regression tests for native notification query results."""

import pytest

from flet_notifications import (
    ActiveNotification,
    AndroidImportance,
    LocalNotifications,
    NotificationError,
    PendingNotification,
)


@pytest.mark.asyncio
async def test_get_pending_hydrates_native_collection():
    """Pending snapshots use native collections and dataclass text defaults."""
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return [
            {"id": 1, "title": "A", "body": "b", "payload": "p"},
            {"id": 2},
            {},
        ]

    service._invoke_method = invoke
    pending = await service.get_pending_notifications()
    assert pending == [
        PendingNotification(id=1, title="A", body="b", payload="p"),
        PendingNotification(id=2),
        PendingNotification(id=0),
    ]


@pytest.mark.asyncio
async def test_get_active_hydrates_native_collection():
    """Active snapshots retain all available fields and fill missing fields."""
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return [
            {
                "id": 2,
                "channel_id": "updates",
                "group_key": "messages",
                "tag": "reply",
                "title": "T",
                "body": "B",
                "payload": "p",
                "big_text": "long",
            },
            {},
        ]

    service._invoke_method = invoke
    active = await service.get_active_notifications()
    assert active == [
        ActiveNotification(
            id=2,
            channel_id="updates",
            group_key="messages",
            tag="reply",
            title="T",
            body="B",
            payload="p",
            big_text="long",
        ),
        ActiveNotification(),
    ]


@pytest.mark.asyncio
async def test_get_channels_hydrates_native_collection():
    """Channels preserve enums, nulls, explicit false flags, and ARGB colors."""
    from flet_notifications import AndroidAudioAttributesUsage, NotificationChannel

    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return [
            {
                "id": "alerts",
                "name": "Alerts",
                "group_id": "updates",
                "importance": "high",
                "description": "Important updates",
                "bypass_dnd": True,
                "play_sound": False,
                "sound": "chime",
                "enable_vibration": False,
                "vibration_pattern": [0, 200, 100, 200],
                "show_badge": False,
                "enable_lights": True,
                "led_color": "#80ff0000",
                "audio_attributes_usage": "alarm",
            },
            {"id": "minimal", "name": "Minimal"},
        ]

    service._invoke_method = invoke
    channels = await service.get_notification_channels()
    assert channels == [
        NotificationChannel(
            id="alerts",
            name="Alerts",
            group_id="updates",
            importance=AndroidImportance.HIGH,
            description="Important updates",
            bypass_dnd=True,
            play_sound=False,
            sound="chime",
            enable_vibration=False,
            vibration_pattern=[0, 200, 100, 200],
            show_badge=False,
            enable_lights=True,
            led_color="#80ff0000",
            audio_attributes_usage=AndroidAudioAttributesUsage.ALARM,
        ),
        NotificationChannel(id="minimal", name="Minimal"),
    ]


@pytest.mark.parametrize(
    "method",
    [
        "get_pending_notifications",
        "get_active_notifications",
        "get_notification_channels",
    ],
)
@pytest.mark.asyncio
async def test_malformed_query_result_raises_query_failed(method):
    """Unexpected response shapes must not silently appear as empty results."""
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return "not json"

    service._invoke_method = invoke
    with pytest.raises(NotificationError) as exc:
        await getattr(service, method)()
    assert exc.value.code == "query_failed"


@pytest.mark.parametrize(
    "method",
    [
        "get_pending_notifications",
        "get_active_notifications",
        "get_notification_channels",
    ],
)
@pytest.mark.asyncio
async def test_empty_query_result_and_native_failure(method):
    """Empty query results and native error codes survive the transport change."""
    service = LocalNotifications()

    async def empty(method_name, arguments=None, timeout=None):
        return []

    service._invoke_method = empty
    assert await getattr(service, method)() == []

    async def failure(method_name, arguments=None, timeout=None):
        return "error:query_failed:permission denied"

    service._invoke_method = failure
    with pytest.raises(NotificationError) as exc:
        await getattr(service, method)()
    assert exc.value.code == "query_failed"
    assert exc.value.message == "permission denied"


@pytest.mark.parametrize(
    "method",
    [
        "get_pending_notifications",
        "get_active_notifications",
        "get_notification_channels",
    ],
)
@pytest.mark.asyncio
async def test_malformed_collection_entry_rejects_the_whole_query(method):
    """A bad row after a valid one must not produce a partial successful result."""
    service = LocalNotifications()
    valid = (
        {"id": "alerts", "name": "Alerts"}
        if method == "get_notification_channels"
        else {"id": 1}
    )
    for entry in [None, [], "invalid", 42]:

        async def invoke(method_name, arguments=None, timeout=None, *, response=entry):
            return [valid, response]

        service._invoke_method = invoke
        with pytest.raises(NotificationError) as exc:
            await getattr(service, method)()
        assert exc.value.code == "query_failed"
        assert "index 1" in exc.value.message


@pytest.mark.asyncio
async def test_channel_reconstruction_errors_are_query_failures():
    """Invalid enum values and missing required fields identify the failing row."""
    service = LocalNotifications()
    for entry in [
        {"id": "alerts", "name": "Alerts", "importance": "invalid"},
        {"id": "alerts"},
    ]:

        async def invoke(method_name, arguments=None, timeout=None, *, response=entry):
            return [{"id": "valid", "name": "Valid"}, response]

        service._invoke_method = invoke
        with pytest.raises(NotificationError) as exc:
            await service.get_notification_channels()
        assert exc.value.code == "query_failed"
        assert "NotificationChannel at index 1" in exc.value.message
        assert isinstance(exc.value.__cause__, (TypeError, ValueError))
