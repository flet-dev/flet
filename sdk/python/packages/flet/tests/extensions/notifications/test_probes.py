"""Regression tests for native notification query results."""

import pytest

from flet_notifications import (
    ActiveNotification,
    AndroidImportance,
    LaunchDetails,
    LocalNotifications,
    NotificationError,
    PendingNotification,
    ResponseType,
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
    ("wire_type", "event_name", "expected"),
    [
        ("tap", "tap", ResponseType.TAP),
        ("action", "action", ResponseType.ACTION),
        ("dismissed", "dismiss", ResponseType.DISMISSED),
    ],
)
@pytest.mark.asyncio
async def test_launch_details_hydrates_response_enum(wire_type, event_name, expected):
    """Launch responses retain enum types, event context, and Windows inputs."""
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return {
            "did_notification_launch_app": True,
            "notification": {
                "id": 9,
                "action_id": "reply",
                "payload": "deep",
                "input": "Hello",
                "data": {"reply": "Hello"},
                "response_type": wire_type,
            },
        }

    service._invoke_method = invoke
    details = await service.get_notification_app_launch_details()
    assert details.did_notification_launch_app is True
    assert details.notification is not None
    assert details.notification.payload == "deep"
    assert details.notification.control is service
    assert details.notification.name == event_name
    assert details.notification.response_type is expected
    assert details.notification.action_id == "reply"
    assert details.notification.input == "Hello"
    assert details.notification.data == {"reply": "Hello"}


@pytest.mark.parametrize("launched", [False, True])
@pytest.mark.asyncio
async def test_launch_details_without_response(launched):
    """A launch flag can be returned without an associated response."""
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return {"did_notification_launch_app": launched, "notification": None}

    service._invoke_method = invoke
    assert await service.get_notification_app_launch_details() == LaunchDetails(
        did_notification_launch_app=launched
    )


@pytest.mark.parametrize(
    "method",
    [
        "get_pending_notifications",
        "get_active_notifications",
        "get_notification_channels",
        "get_notification_app_launch_details",
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
        "get_notification_app_launch_details",
    ],
)
@pytest.mark.asyncio
async def test_empty_query_result_and_native_failure(method):
    """Empty query results and native error codes survive the transport change."""
    service = LocalNotifications()

    async def empty(method_name, arguments=None, timeout=None):
        return {} if method == "get_notification_app_launch_details" else []

    service._invoke_method = empty
    expected = (
        LaunchDetails() if method == "get_notification_app_launch_details" else []
    )
    assert await getattr(service, method)() == expected

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


@pytest.mark.asyncio
async def test_malformed_launch_fields_are_query_failures():
    """Wrong flag or response shapes cannot masquerade as launch snapshots."""
    service = LocalNotifications()
    for result in [
        {"did_notification_launch_app": "false"},
        {"did_notification_launch_app": 1},
        {"did_notification_launch_app": None},
        {"notification": []},
        {"notification": False},
        {"notification": "invalid"},
        {"notification": {"response_type": []}},
        {"notification": {"response_type": "unknown"}},
    ]:

        async def invoke(method_name, arguments=None, timeout=None, *, response=result):
            return response

        service._invoke_method = invoke
        with pytest.raises(NotificationError) as exc:
            await service.get_notification_app_launch_details()
        assert exc.value.code == "query_failed"
