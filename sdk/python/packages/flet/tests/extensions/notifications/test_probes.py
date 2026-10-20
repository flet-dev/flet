"""Regression tests for native notification query results."""

import json

import pytest

from flet_notifications import (
    ActiveNotification,
    Importance,
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
            None,
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
            None,
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
async def test_get_channels_decodes_json_string():
    from flet_notifications import NotificationChannel

    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return json.dumps(
            [
                {
                    "id": "alerts",
                    "name": "Alerts",
                    "groupId": "updates",
                    "importance": "high",
                }
            ]
        )

    service._invoke_method = invoke
    channels = await service.get_notification_channels()
    assert channels == [
        NotificationChannel(
            id="alerts", name="Alerts", group_id="updates", importance=Importance.HIGH
        )
    ]


@pytest.mark.asyncio
async def test_launch_details_decodes_json_string():
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return json.dumps(
            {
                "did_notification_launch_app": True,
                "notification": {
                    "id": 9,
                    "action_id": "open",
                    "payload": "deep",
                    "input": "",
                    "response_type": "action",
                },
            }
        )

    service._invoke_method = invoke
    details = await service.get_notification_app_launch_details()
    assert details.did_notification_launch_app is True
    assert details.notification is not None
    assert details.notification.payload == "deep"


@pytest.mark.parametrize(
    "method", ["get_pending_notifications", "get_active_notifications"]
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
    "method", ["get_pending_notifications", "get_active_notifications"]
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
