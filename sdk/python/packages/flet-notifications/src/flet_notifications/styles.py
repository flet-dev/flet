"""Rich notification styles (big text, big picture, inbox, messaging)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class AndroidIcon:
    """An Android notification icon or image.

    Exactly one source must be set: a bundled drawable resource name, a file
    path, a content URI, a Flutter asset path, or raw bytes (base64).
    """

    drawable_resource: str | None = None
    file_path: str | None = None
    content_uri: str | None = None
    flutter_asset: str | None = None
    data_base64: str | None = None

    def __post_init__(self) -> None:
        sources = [
            self.drawable_resource,
            self.file_path,
            self.content_uri,
            self.flutter_asset,
            self.data_base64,
        ]
        if sum(s is not None for s in sources) != 1:
            raise ValueError("AndroidIcon requires exactly one source")

    def to_dict(self) -> dict:
        return {
            "drawable_resource": self.drawable_resource,
            "file_path": self.file_path,
            "content_uri": self.content_uri,
            "flutter_asset": self.flutter_asset,
            "data_base64": self.data_base64,
        }


@dataclass(kw_only=True)
class BigTextStyle:
    """Expandable text (the Android "big text" style)."""

    big_text: str
    content_title: str | None = None
    summary_text: str | None = None

    def to_dict(self) -> dict:
        return {
            "type": "big_text",
            "big_text": self.big_text,
            "content_title": self.content_title,
            "summary_text": self.summary_text,
        }


@dataclass(kw_only=True)
class BigPictureStyle:
    """Expandable image (the Android "big picture" style)."""

    image: AndroidIcon
    large_icon: AndroidIcon | None = None
    content_title: str | None = None
    summary_text: str | None = None

    def to_dict(self) -> dict:
        return {
            "type": "big_picture",
            "image": self.image.to_dict(),
            "large_icon": self.large_icon.to_dict() if self.large_icon else None,
            "content_title": self.content_title,
            "summary_text": self.summary_text,
        }


@dataclass(kw_only=True)
class InboxStyle:
    """Up to seven expandable lines (the Android "inbox" style)."""

    lines: list[str] = field(default_factory=list)
    content_title: str | None = None
    summary_text: str | None = None

    def __post_init__(self) -> None:
        if not self.lines:
            raise ValueError("InboxStyle requires at least one line")

    def to_dict(self) -> dict:
        return {
            "type": "inbox",
            "lines": list(self.lines),
            "content_title": self.content_title,
            "summary_text": self.summary_text,
        }


@dataclass(kw_only=True)
class Person:
    """A participant in a messaging-style conversation."""

    name: str
    key: str | None = None
    bot: bool = False
    important: bool = False
    uri: str | None = None
    icon: AndroidIcon | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "key": self.key,
            "bot": self.bot,
            "important": self.important,
            "uri": self.uri,
            "icon": self.icon.to_dict() if self.icon else None,
        }


@dataclass(kw_only=True)
class Message:
    """One message in a messaging-style conversation."""

    text: str
    timestamp: datetime
    person: Person

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "person": self.person.to_dict(),
        }


@dataclass(kw_only=True)
class MessagingStyle:
    """Chat conversation (the Android/iOS messaging style)."""

    person: Person
    messages: list[Message] = field(default_factory=list)
    conversation_title: str | None = None
    group_conversation: bool = False

    def to_dict(self) -> dict:
        return {
            "type": "messaging",
            "person": self.person.to_dict(),
            "messages": [m.to_dict() for m in self.messages],
            "conversation_title": self.conversation_title,
            "group_conversation": self.group_conversation,
        }


Style = BigTextStyle | BigPictureStyle | InboxStyle | MessagingStyle
"""Union of the supported notification styles."""
