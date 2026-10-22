"""Tests for notification styles."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    AndroidBigPictureStyle,
    AndroidBigTextStyle,
    AndroidBytesBitmap,
    AndroidContentUriIcon,
    AndroidDrawableBitmap,
    AndroidFileBitmap,
    AndroidInboxStyle,
    AndroidMessage,
    AndroidMessagingStyle,
    AndroidOptions,
    AndroidPerson,
    LocalNotifications,
    NotificationOptions,
    RepeatInterval,
)

from .helpers import encode_wire


@pytest.mark.parametrize(
    ("style", "kind"),
    [
        (AndroidBigTextStyle(big_text="Long text"), "big_text"),
        (
            AndroidBigPictureStyle(image=AndroidFileBitmap(path="/tmp/photo.png")),
            "big_picture",
        ),
        (AndroidInboxStyle(lines=["one"]), "inbox"),
        (AndroidMessagingStyle(person=AndroidPerson(name="Ada")), "messaging"),
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
    person = AndroidPerson(name="Ada")
    message = AndroidMessage(
        text="Hi",
        timestamp=datetime(
            2030, 1, 1, 10, 0, tzinfo=timezone(timedelta(hours=5, minutes=30))
        ),
        person=person,
    )
    options = NotificationOptions(
        android=AndroidOptions(
            style=AndroidMessagingStyle(person=person, messages=[message])
        )
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


def test_icon_sources_encode_discriminators_and_raw_bytes():
    """Icon sources carry their kind, and byte sources travel as raw bytes."""
    assert encode_wire(AndroidDrawableBitmap(name="avatar")) == {
        "_type": "drawable",
        "name": "avatar",
    }
    assert encode_wire(AndroidBytesBitmap(data=b"\x01\x02")) == {
        "_type": "bytes",
        "data": b"\x01\x02",
    }
    assert encode_wire(AndroidContentUriIcon(uri="content://x")) == {
        "_type": "content_uri",
        "uri": "content://x",
    }
