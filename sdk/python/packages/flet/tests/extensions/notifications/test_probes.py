"""Regression tests for native JSON query results."""

import json

import pytest

from flet_notifications import (
    Importance,
    LocalNotifications,
    NotificationError,
    PendingNotification,
)


@pytest.mark.asyncio
async def test_get_pending_decodes_json_string():
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return json.dumps([{"id": 1, "title": "A", "body": "b", "payload": "p"}])

    service._invoke_method = invoke
    pending = await service.get_pending_notifications()
    assert pending == [PendingNotification(id=1, title="A", body="b", payload="p")]


@pytest.mark.asyncio
async def test_get_active_decodes_json_string():
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return json.dumps([{"id": 2, "title": "T", "payload": "p", "big_text": "long"}])

    service._invoke_method = invoke
    active = await service.get_active_notifications()
    assert active[0].id == 2
    assert active[0].big_text == "long"


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


@pytest.mark.asyncio
async def test_malformed_json_raises_query_failed():
    service = LocalNotifications()

    async def invoke(method_name, arguments=None, timeout=None):
        return "not json"

    service._invoke_method = invoke
    with pytest.raises(NotificationError) as exc:
        await service.get_pending_notifications()
    assert exc.value.code == "query_failed"
