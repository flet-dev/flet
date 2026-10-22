from abc import ABC, abstractmethod
from dataclasses import field
from datetime import datetime

import flet as ft

__all__ = [
    "AndroidBigPictureStyle",
    "AndroidBigTextStyle",
    "AndroidIcon",
    "AndroidInboxStyle",
    "AndroidMessage",
    "AndroidMessagingStyle",
    "AndroidPerson",
    "AndroidStyle",
]


@ft.value(kw_only=True)
class AndroidStyle(ABC):
    """
    Abstract base for rich Android notification layouts.

    Pass a concrete :class:`flet_notifications.AndroidBigTextStyle`,
    :class:`flet_notifications.AndroidBigPictureStyle`,
    :class:`flet_notifications.AndroidInboxStyle`, or
    :class:`flet_notifications.AndroidMessagingStyle` as
    :attr:`flet_notifications.AndroidOptions.style`.

    Note:
        Rich layouts are supported only on Android. Other platforms use their normal
        notification presentation.
    """

    _type: str = field(init=False, repr=False, compare=False)

    @abstractmethod
    def __post_init__(self) -> None:
        """Set the concrete style's discriminator."""


@ft.value(kw_only=True)
class AndroidIcon:
    """
    Image source for an Android person icon or big-picture bitmap.

    Set exactly one source. :attr:`flet_notifications.AndroidPerson.icon` supports all
    five sources; :class:`flet_notifications.AndroidBigPictureStyle` supports only
    drawable resources, file paths, and base64-encoded bytes. Paths and URIs refer to
    the Android device, not the Python server.

    Raises:
        ValueError: If zero or multiple sources are provided.
    """

    drawable_resource: str | None = None
    """
    Name of an image in the app's Android drawable resources.

    For example, `"contact_avatar"`, without the file extension.
    """

    file_path: str | None = None
    """Absolute path of an image file accessible to the app on the Android device."""

    content_uri: str | None = None
    """
    Android `content://` URI used as a person's icon.

    Note:
        The app must have permission to read it. Not supported by
        :class:`flet_notifications.AndroidBigPictureStyle`.
    """

    flutter_asset: str | None = None
    """
    Flutter bitmap-asset path used as a person's icon.

    Note:
        The asset must be bundled in the app. Not supported by
        :class:`flet_notifications.AndroidBigPictureStyle`.
    """

    data_base64: str | None = None
    """
    Base64-encoded image bytes, without a data-URL prefix.

    For example, `base64.b64encode(image_bytes).decode("ascii")`. Supported by both
    person icons and big-picture bitmaps.
    """

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
class AndroidBigTextStyle(AndroidStyle):
    """
    Expanded Android notification layout displaying a longer body.

    Note:
        The normal notification `body` remains the collapsed text. Android chooses how
        much expanded text fits. Other platforms ignore this style.
    """

    big_text: str
    """Nonempty text displayed when the Android notification is expanded."""

    content_title: str | None = None
    """
    Title used in the expanded layout instead of the notification title.

    `None` keeps the normal title.
    """

    summary_text: str | None = None
    """Optional summary displayed with the expanded notification."""

    def __post_init__(self) -> None:
        self._type = "big_text"


@ft.value(kw_only=True)
class AndroidBigPictureStyle(AndroidStyle):
    """
    Expanded Android notification layout displaying a large image.

    Note:
        Uses drawable, device-file, or base64-byte image sources. Content URIs and
        Flutter assets are not accepted by this layout. Other platforms ignore it.
    """

    image: AndroidIcon
    """Image displayed in the expanded notification."""

    large_icon: AndroidIcon | None = None
    """
    Optional large icon for the expanded notification.

    Supports the same bitmap sources as :attr:`image`.
    """

    content_title: str | None = None
    """Optional replacement title for the expanded layout."""

    summary_text: str | None = None
    """Optional summary displayed with the expanded image."""

    def __post_init__(self) -> None:
        self._type = "big_picture"


@ft.value(kw_only=True)
class AndroidInboxStyle(AndroidStyle):
    """
    Expanded Android notification layout showing a list of text lines.

    Android displays up to seven lines in this layout. Supply a shorter summary as the
    normal notification `body` for the collapsed view.

    Raises:
        ValueError: If :attr:`lines` is empty.
    """

    lines: list[str] = field(default_factory=list)
    """Nonempty list of lines to display when the notification is expanded."""

    content_title: str | None = None
    """Optional replacement title for the expanded layout."""

    summary_text: str | None = None
    """Optional summary displayed below the expanded lines."""

    def __post_init__(self) -> None:
        self._type = "inbox"
        if not self.lines:
            raise ValueError("AndroidInboxStyle requires at least one line")


@ft.value(kw_only=True)
class AndroidPerson:
    """
    Participant identity used by an Android messaging-style notification.

    Use a consistent :attr:`key` or :attr:`uri` to identify the same person across
    notifications, even when their display name changes.
    """

    name: str
    """Nonempty display name of the participant."""

    key: str | None = None
    """Stable identifier distinguishing this person from others."""

    bot: bool = False
    """Whether the participant represents a bot rather than a human."""

    important: bool = False
    """Whether Android should treat this as an important participant."""

    uri: str | None = None
    """
    URI identifying the participant, such as `"mailto:alex@example.com"`.

    A matching contact URI can help Android associate notifications with contacts.
    """

    icon: AndroidIcon | None = None
    """
    Optional participant avatar, supporting any \
    :class:`flet_notifications.AndroidIcon` source.
    """


@ft.value(kw_only=True)
class AndroidMessage:
    """
    Message displayed in an Android :class:`flet_notifications.AndroidMessagingStyle` \
    conversation.
    """

    text: str
    """Text content of the message."""

    timestamp: datetime
    """
    Time the message arrived.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """

    person: AndroidPerson
    """
    Participant who sent this message.

    Note:
        For an outgoing message, pass the same participant used as
        :attr:`flet_notifications.AndroidMessagingStyle.person`; this API requires an
        explicit person.
    """


@ft.value(kw_only=True)
class AndroidMessagingStyle(AndroidStyle):
    """
    Android notification layout for a conversation and its recent messages.

    The bridge does not apply this style on iOS or macOS. Those platforms can use
    :attr:`flet_notifications.DarwinOptions.thread_identifier` for grouping.
    """

    person: AndroidPerson
    """Identity of the local user receiving or participating in the conversation."""

    messages: list[AndroidMessage] = field(default_factory=list)
    """
    Messages to show in the conversation.

    Supply messages in chronological order, including recent history when updating the
    same notification. An empty list supplies no message history.
    """

    conversation_title: str | None = None
    """
    Title identifying the conversation, especially for group conversations.

    Normally omit for a one-to-one conversation, where the participant name identifies
    the chat.
    """

    group_conversation: bool = False
    """Whether the conversation contains multiple other participants."""

    def __post_init__(self) -> None:
        self._type = "messaging"
