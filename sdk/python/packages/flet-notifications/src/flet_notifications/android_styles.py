from abc import ABC, abstractmethod
from dataclasses import field
from datetime import datetime
from typing import Annotated

import flet as ft
from flet.utils.validation import V

__all__ = [
    "AndroidBigPictureStyle",
    "AndroidBigTextStyle",
    "AndroidBitmap",
    "AndroidBytesBitmap",
    "AndroidContentUriIcon",
    "AndroidDrawableBitmap",
    "AndroidFileBitmap",
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
class AndroidIcon(ABC):
    """
    Abstract base for Android image sources.

    :attr:`flet_notifications.AndroidPerson.icon` accepts any concrete source:
    :class:`flet_notifications.AndroidDrawableBitmap`,
    :class:`flet_notifications.AndroidFileBitmap`,
    :class:`flet_notifications.AndroidBytesBitmap`, or
    :class:`flet_notifications.AndroidContentUriIcon`. Notification images accept only
    the :class:`flet_notifications.AndroidBitmap` sources.
    """

    _type: str = field(init=False, repr=False, compare=False)

    @abstractmethod
    def __post_init__(self) -> None:
        """Set the concrete source's discriminator."""


@ft.value(kw_only=True)
class AndroidBitmap(AndroidIcon, ABC):
    """
    Abstract base for Android image sources that can be decoded into a bitmap.

    Accepted by :attr:`flet_notifications.AndroidOptions.large_icon` and
    :class:`flet_notifications.AndroidBigPictureStyle`, as well as anywhere an
    :class:`flet_notifications.AndroidIcon` is accepted.

    :class:`flet_notifications.AndroidBytesBitmap` works wherever the Python code
    runs and suits most images. :class:`flet_notifications.AndroidFileBitmap` needs a
    file on the device, and :class:`flet_notifications.AndroidDrawableBitmap` an image
    bundled with the app.
    """


@ft.value(kw_only=True)
class AndroidDrawableBitmap(AndroidBitmap):
    """
    Image from the app's Android drawable resources.

    Add the image with the
    [`res_dir`](https://flet.dev/docs/publish/android#resources) build setting,
    for example as `drawable/promo_banner.png`.
    """

    name: str
    """
    Resource name, without the file extension.

    For example, `"contact_avatar"` for `res/drawable/contact_avatar.png`.
    """

    def __post_init__(self) -> None:
        self._type = "drawable"


@ft.value(kw_only=True)
class AndroidFileBitmap(AndroidBitmap):
    """
    Image file on the Android device.

    In a built app, files in the app's assets directory are available on the device,
    for example at `Path(__file__).parent / "assets" / "avatar.png"`; files the app
    saves, such as under a :class:`flet.StoragePaths` directory, can also be used.

    Note:
        The path must exist on the Android device. While developing with
        [`flet run`](https://flet.dev/docs/cli/flet-run/) against a phone, Python runs
        on your computer, so its paths do not exist on the device; use
        :class:`flet_notifications.AndroidBytesBitmap` instead.
    """

    path: str
    """Absolute path of an image file readable by the app."""

    def __post_init__(self) -> None:
        self._type = "file"


@ft.value(kw_only=True)
class AndroidBytesBitmap(AndroidBitmap):
    """
    Image from encoded bytes, such as the contents of a PNG or JPEG file.

    The bytes travel with the notification request, so this source works wherever the
    Python code runs, including [`flet run`](https://flet.dev/docs/cli/flet-run/)
    against a phone. Prefer it for images shipped with the app or downloaded at
    runtime.

    Example:
        ```python
        from pathlib import Path

        import flet_notifications as ftn

        avatar = ftn.AndroidBytesBitmap(
            data=(Path(__file__).parent / "assets" / "avatar.png").read_bytes()
        )
        ```
    """

    data: bytes
    """Encoded image bytes."""

    def __post_init__(self) -> None:
        self._type = "bytes"


@ft.value(kw_only=True)
class AndroidContentUriIcon(AndroidIcon):
    """
    Image identified by an Android `content://` URI.

    Note:
        Supported only by :attr:`flet_notifications.AndroidPerson.icon`. The app must
        have permission to read the URI.
    """

    uri: str
    """Content URI of the image, such as `"content://contacts/people/1/photo"`."""

    def __post_init__(self) -> None:
        self._type = "content_uri"


@ft.value(kw_only=True)
class AndroidBigTextStyle(AndroidStyle):
    """
    Expanded Android notification layout displaying a longer body.

    Note:
        The normal notification `body` remains the collapsed text. Android chooses how
        much expanded text fits. Other platforms ignore this style.
    """

    text: str
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
        Other platforms ignore this style.
    """

    image: AndroidBitmap
    """Image displayed in the expanded notification."""

    large_icon: AndroidBitmap | None = None
    """
    Large icon shown while the notification is expanded.

    `None` keeps the notification's
    :attr:`~flet_notifications.AndroidOptions.large_icon`.
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

    lines: Annotated[list[str], V.non_empty()] = field(default_factory=list)
    """Nonempty list of lines to display when the notification is expanded."""

    content_title: str | None = None
    """Optional replacement title for the expanded layout."""

    summary_text: str | None = None
    """Optional summary displayed below the expanded lines."""

    def __post_init__(self) -> None:
        self._type = "inbox"


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
    Optional participant avatar, supporting any
    :class:`flet_notifications.AndroidIcon` source.
    """


@ft.value(kw_only=True)
class AndroidMessage:
    """
    Message displayed in an Android :class:`flet_notifications.AndroidMessagingStyle`
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
