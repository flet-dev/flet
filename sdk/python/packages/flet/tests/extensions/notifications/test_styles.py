"""Tests for notification styles."""

from datetime import datetime, timedelta, timezone

import pytest

from flet_notifications import (
    AndroidIcon,
    BigPictureStyle,
    BigTextStyle,
    InboxStyle,
    Message,
    MessagingStyle,
    Person,
)
from flet_notifications.styles import prepare_style

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
    payload = encode_wire(prepare_style(style))
    assert payload["_type"] == kind
    assert "type" not in payload


@pytest.mark.parametrize(
    "timestamp",
    [
        datetime(2030, 1, 1, 10, 0),
        datetime(2030, 1, 1, 10, 0, tzinfo=timezone(timedelta(hours=5, minutes=30))),
    ],
)
def test_message_timestamp_preserves_wall_clock_and_offset(timestamp):
    person = Person(name="Ada")
    message = Message(text="Hi", timestamp=timestamp, person=person)
    style = MessagingStyle(person=person, messages=[message])
    assert encode_wire(prepare_style(style))["messages"][0]["timestamp"] == (
        timestamp.isoformat()
    )
    message.timestamp += timedelta(minutes=1)
    assert encode_wire(prepare_style(style))["messages"][0]["timestamp"] == (
        message.timestamp.isoformat()
    )
