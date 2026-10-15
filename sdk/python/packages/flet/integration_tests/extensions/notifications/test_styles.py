"""Tests for notification styles."""

from datetime import datetime

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


def test_android_icon_requires_exactly_one_source():
    with pytest.raises(ValueError, match="exactly one"):
        AndroidIcon()
    with pytest.raises(ValueError, match="exactly one"):
        AndroidIcon(drawable_resource="ic", file_path="/tmp/x.png")


def test_android_icon_sources():
    assert AndroidIcon(drawable_resource="ic_star").to_dict() == {
        "drawable_resource": "ic_star",
        "file_path": None,
        "content_uri": None,
        "flutter_asset": None,
        "data_base64": None,
    }
    assert AndroidIcon(flutter_asset="assets/a.png").to_dict()["flutter_asset"] == (
        "assets/a.png"
    )


def test_big_text_style_to_dict():
    style = BigTextStyle(
        big_text="Long text", content_title="Title", summary_text="Summary"
    )
    assert style.to_dict() == {
        "type": "big_text",
        "big_text": "Long text",
        "content_title": "Title",
        "summary_text": "Summary",
    }


def test_big_picture_style_to_dict():
    style = BigPictureStyle(
        image=AndroidIcon(file_path="/tmp/photo.jpg"),
        large_icon=AndroidIcon(drawable_resource="ic"),
        summary_text="2 photos",
    )
    d = style.to_dict()
    assert d["type"] == "big_picture"
    assert d["image"] == AndroidIcon(file_path="/tmp/photo.jpg").to_dict()
    assert d["large_icon"]["drawable_resource"] == "ic"
    assert d["summary_text"] == "2 photos"


def test_inbox_style_requires_lines():
    with pytest.raises(ValueError, match="at least one line"):
        InboxStyle(lines=[])
    style = InboxStyle(lines=["one", "two"])
    assert style.to_dict()["lines"] == ["one", "two"]


def test_messaging_style_to_dict():
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
    d = style.to_dict()
    assert d["type"] == "messaging"
    assert d["person"] == person.to_dict()
    assert d["person"]["name"] == "Ada"
    assert d["messages"][0]["timestamp"] == "2030-01-01T10:00:00"
    assert d["conversation_title"] == "Team chat"
    assert d["group_conversation"] is True


def test_person_to_dict():
    person = Person(name="Bob", key="b1", bot=True, uri="tel:123")
    assert person.to_dict() == {
        "name": "Bob",
        "key": "b1",
        "bot": True,
        "important": False,
        "uri": "tel:123",
        "icon": None,
    }


def test_style_union_membership():
    assert isinstance(BigTextStyle(big_text="x"), Style)
    assert isinstance(InboxStyle(lines=["a"]), Style)
