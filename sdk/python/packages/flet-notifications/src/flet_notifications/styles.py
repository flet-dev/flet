"""Rich notification styles (big text, big picture, inbox, messaging)."""

from dataclasses import field
from datetime import datetime

import flet as ft


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
class BigTextStyle:
    """Expandable text (the Android "big text" style)."""

    big_text: str
    content_title: str | None = None
    summary_text: str | None = None
    _type: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._type = "big_text"


@ft.value(kw_only=True)
class BigPictureStyle:
    """Expandable image (the Android "big picture" style)."""

    image: AndroidIcon
    large_icon: AndroidIcon | None = None
    content_title: str | None = None
    summary_text: str | None = None
    _type: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._type = "big_picture"


@ft.value(kw_only=True)
class InboxStyle:
    """Up to seven expandable lines (the Android "inbox" style)."""

    lines: list[str] = field(default_factory=list)
    content_title: str | None = None
    summary_text: str | None = None
    _type: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._type = "inbox"
        if not self.lines:
            raise ValueError("InboxStyle requires at least one line")


@ft.value(kw_only=True)
class Person:
    """A participant in a messaging-style conversation."""

    name: str
    key: str | None = None
    bot: bool = False
    important: bool = False
    uri: str | None = None
    icon: AndroidIcon | None = None


@ft.value(kw_only=True)
class Message:
    """One message in a messaging-style conversation."""

    text: str
    timestamp: datetime
    person: Person


@ft.value(kw_only=True)
class MessagingStyle:
    """Chat conversation (the Android/iOS messaging style)."""

    person: Person
    messages: list[Message] = field(default_factory=list)
    conversation_title: str | None = None
    group_conversation: bool = False

    _type: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self._type = "messaging"


Style = BigTextStyle | BigPictureStyle | InboxStyle | MessagingStyle
"""Union of the supported notification styles."""


def prepare_style(style: Style | None) -> Style | dict | None:
    """Preserve message wall-clock timestamps while Flet encodes nested values.

    The native parser expects ISO text. Flet's datetime codec normalizes naive
    datetimes to the Python host's timezone, which would change their existing
    interpretation in the notification device's local timezone.
    """
    if not isinstance(style, MessagingStyle):
        return style
    return {
        "_type": style._type,
        "person": style.person,
        "messages": [
            {
                "text": message.text,
                "timestamp": message.timestamp.isoformat(),
                "person": message.person,
            }
            for message in style.messages
        ],
        "conversation_title": style.conversation_title,
        "group_conversation": style.group_conversation,
    }
