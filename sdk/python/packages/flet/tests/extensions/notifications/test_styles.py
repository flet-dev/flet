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
    Style,
)
from flet_notifications.styles import prepare_style

from .helpers import encode_wire


def test_android_icon_requires_exactly_one_source():
    with pytest.raises(ValueError, match="exactly one"):
        AndroidIcon()
    with pytest.raises(ValueError, match="exactly one"):
        AndroidIcon(drawable_resource="ic", file_path="/tmp/x.png")


def test_android_icon_sources():
    assert encode_wire(AndroidIcon(drawable_resource="ic_star")) == {
        "drawable_resource": "ic_star",
    }
    assert encode_wire(AndroidIcon(flutter_asset="assets/a.png"))["flutter_asset"] == (
        "assets/a.png"
    )


def test_big_text_style_wire_payload():
    style = BigTextStyle(
        big_text="Long text", content_title="Title", summary_text="Summary"
    )
    assert encode_wire(style) == {
        "_type": "big_text",
        "big_text": "Long text",
        "content_title": "Title",
        "summary_text": "Summary",
    }


def test_big_picture_style_wire_payload():
    style = BigPictureStyle(
        image=AndroidIcon(file_path="/tmp/photo.jpg"),
        large_icon=AndroidIcon(drawable_resource="ic"),
        summary_text="2 photos",
    )
    d = encode_wire(style)
    assert d["_type"] == "big_picture"
    assert d["image"] == encode_wire(AndroidIcon(file_path="/tmp/photo.jpg"))
    assert d["large_icon"]["drawable_resource"] == "ic"
    assert d["summary_text"] == "2 photos"


def test_inbox_style_requires_lines():
    with pytest.raises(ValueError, match="at least one line"):
        InboxStyle(lines=[])
    style = InboxStyle(lines=["one", "two"])
    assert encode_wire(style)["lines"] == ["one", "two"]


def test_messaging_style_wire_payload():
    person = Person(name="Ada")
    style = MessagingStyle(
        person=person,
        messages=[
            Message(
                text="hi",
                timestamp=datetime(2030, 1, 1, 10, 0),
                person=person,
            )
        ],
        conversation_title="Team chat",
        group_conversation=True,
    )
    d = encode_wire(prepare_style(style))
    assert d["_type"] == "messaging"
    assert d["person"] == encode_wire(person)
    assert d["person"]["name"] == "Ada"
    assert d["messages"][0]["timestamp"] == "2030-01-01T10:00:00"
    assert d["conversation_title"] == "Team chat"
    assert d["group_conversation"] is True


def test_person_wire_payload():
    person = Person(name="Bob", key="b1", bot=True, uri="tel:123")
    assert encode_wire(person) == {
        "name": "Bob",
        "key": "b1",
        "bot": True,
        "uri": "tel:123",
    }


def test_style_union_membership():
    assert isinstance(BigTextStyle(big_text="x"), Style)
    assert isinstance(InboxStyle(lines=["a"]), Style)


@pytest.mark.parametrize(
    ("style", "kind"),
    [
        (BigTextStyle(big_text="Long text"), "big_text"),
        (BigPictureStyle(image=AndroidIcon(file_path="/tmp/photo.png")), "big_picture"),
        (InboxStyle(lines=["one"]), "inbox"),
        (MessagingStyle(person=Person(name="Ada")), "messaging"),
    ],
)
def test_style_discriminator_is_private_and_serialized(style, kind):
    assert not hasattr(style, "type")
    assert style._type == kind
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
