from enum import Enum
from typing import Annotated

import flet as ft
from flet_notifications.validation import non_negative_duration

__all__ = [
    "LinuxCategory",
    "LinuxOptions",
    "LinuxUrgency",
]


class LinuxUrgency(Enum):
    """
    Urgency hint sent to the Linux desktop notification server.

    Note:
        The server decides how to display notifications and may ignore hints.
    """

    LOW = "low"
    """Uses low urgency for information that does not require immediate attention."""

    NORMAL = "normal"
    """Uses normal urgency for an ordinary notification."""

    CRITICAL = "critical"
    """
    Uses critical urgency for information requiring immediate attention.

    A conforming server should keep critical notifications visible until dismissed, but
    desktop-specific behavior can vary.
    """


class LinuxCategory(Enum):
    """
    Freedesktop category hint used by a Linux notification server.

    Note:
        Set :attr:`flet_notifications.LinuxOptions.category`. The desktop notification
        server decides how to filter or present each category and may ignore the hint.
    """

    DEVICE = "device"
    """Device-related notification that does not fit a more specific category."""

    DEVICE_ADDED = "device.added"
    """A device, such as a USB drive, was connected."""

    DEVICE_ERROR = "device.error"
    """A device encountered an error."""

    DEVICE_REMOVED = "device.removed"
    """A device was disconnected."""

    EMAIL = "email"
    """Email-related notification without a more specific category."""

    EMAIL_ARRIVED = "email.arrived"
    """A new email arrived."""

    EMAIL_BOUNCED = "email.bounced"
    """An email could not be delivered and bounced."""

    IM = "im"
    """Instant-message notification without a more specific category."""

    IM_ERROR = "im.error"
    """An instant-messaging error occurred."""

    IM_RECEIVED = "im.received"
    """An instant message arrived."""

    NETWORK = "network"
    """Network-related notification without a more specific category."""

    NETWORK_CONNECTED = "network.connected"
    """A network connection was established."""

    NETWORK_DISCONNECTED = "network.disconnected"
    """A network connection was lost or closed."""

    NETWORK_ERROR = "network.error"
    """A network connection or operation failed."""

    PRESENCE = "presence"
    """A presence status changed, such as becoming idle or away."""

    PRESENCE_OFFLINE = "presence.offline"
    """A contact or account went offline."""

    PRESENCE_ONLINE = "presence.online"
    """A contact or account came online."""

    TRANSFER = "transfer"
    """File-transfer notification without a more specific category."""

    TRANSFER_COMPLETE = "transfer.complete"
    """A file transfer or download completed."""

    TRANSFER_ERROR = "transfer.error"
    """A file transfer or download failed."""


@ft.value(kw_only=True)
class LinuxOptions:
    """
    Hints for a Linux freedesktop notification server.

    Note:
        Feature support varies by desktop and notification daemon. Unsupported hints may
        be ignored. This extension does not expose server-capability queries.
    """

    icon: str | None = None
    """
    Theme icon name or absolute device file path.

    The bridge also recognizes a `file://` prefix as a file-icon source; theme names
    such as `"dialog-information"` use the desktop's installed icon theme.
    """

    sound: str | None = None
    """Name of a sound from the desktop sound theme, such as `"message"`."""

    category: LinuxCategory | None = None
    """
    Category hint used by the server to classify the notification.

    Note:
        See :class:`~flet_notifications.LinuxCategory`. The notification
        server determines the presentation and may ignore this hint.
    """

    urgency: LinuxUrgency | None = None
    """Urgency hint."""

    timeout: Annotated[ft.DurationValue | None, non_negative_duration(-1)] = None
    """
    Requested time to keep the notification visible.

    Integer values are interpreted as milliseconds. `None` or `-1` uses the notification
    server's timeout; `0` requests no expiry.

    Note:
        The server can ignore this hint or apply its own policy, especially for critical
        notifications.
    """

    resident: bool | None = None
    """
    Whether to retain the notification after an action is invoked.

    Note:
        The user or application must remove resident notifications; requires persistence
        support from the notification server.
    """

    transient: bool | None = None
    """
    Whether to bypass notification history or persistence.

    Note:
        Requires support from the desktop notification server.
    """

    silent: bool | None = None
    """
    Whether to ask the server to suppress notification sounds.

    Useful when the application plays its own sound.
    """

    action_key_as_icon_name: bool | None = None
    """
    Whether to show action buttons as icons.

    The notification server reads each
    :attr:`flet_notifications.NotificationAction.id` as an icon name from the desktop's
    icon theme, such as `"mail-reply-sender"`, and uses the action's title as the icon's
    accessible label.

    Note:
        Requires support from the desktop notification server.
    """
