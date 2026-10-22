"""Tests for notification styles."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    AndroidIcon,
    AndroidOptions,
    BigPictureStyle,
    BigTextStyle,
    InboxStyle,
    LocalNotifications,
    Message,
    MessagingStyle,
    NotificationOptions,
    Person,
    RepeatInterval,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    ("style", "kind"),
    [
        (BigTextStyle(big_text="Long text"), "big_text"),
        (BigPictureStyle(image=AndroidIcon(file_path="/tmp/photo.png")), "big_picture"),
        (InboxStyle(lines=["one"]), "inbox"),
        (MessagingStyle(person=Person(name="Ada")), "messaging"),
    ],
)
def test_styles_encode_native_discriminators(style, kind):
    """Each concrete style is encoded with the discriminator Dart switches on."""
    payload = encode_wire(style)
    assert payload["_type"] == kind
    assert "type" not in payload


@pytest.mark.parametrize(
    "method_name", ["show", "schedule", "periodically_show", "start_foreground_service"]
)
@pytest.mark.asyncio
async def test_message_timestamp_preserves_instant(method_name):
    """Every notification method sends current message times as exact instants."""
    person = Person(name="Ada")
    message = Message(
        text="Hi",
        timestamp=datetime(
            2030, 1, 1, 10, 0, tzinfo=timezone(timedelta(hours=5, minutes=30))
        ),
        person=person,
    )
    options = NotificationOptions(
        android=AndroidOptions(style=MessagingStyle(person=person, messages=[message]))
    )
    service = LocalNotifications()
    calls = []

    async def invoke(name, arguments=None, timeout=None):
        calls.append(encode_wire(arguments))
        return "ok"

    service._invoke_method = invoke
    kwargs = {"id": 1, "options": options}
    if method_name == "schedule":
        kwargs["when"] = timedelta(seconds=30)
    elif method_name == "periodically_show":
        kwargs["repeat_interval"] = RepeatInterval.HOURLY
    for _ in range(2):
        await getattr(service, method_name)(**kwargs)
        style = calls[-1]["options"]["android"]["style"]
        assert style["messages"][0]["timestamp"] == message.timestamp
        message.timestamp += timedelta(minutes=1)
