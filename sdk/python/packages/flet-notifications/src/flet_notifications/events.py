from dataclasses import dataclass

from flet_notifications.base import NotificationEvent

__all__ = [
    "ActiveNotification",
    "LaunchDetails",
    "PendingNotification",
]


@dataclass
class PendingNotification:
    """
    Notification scheduled for future delivery.

    Returned by
    :meth:`flet_notifications.LocalNotifications.get_pending_notifications`. This is a
    query snapshot, not an editable schedule; changing its fields does not update or
    cancel the native request. Unavailable text values become empty strings.
    """

    id: int
    """Identifier supplied when scheduling the notification."""

    title: str = ""
    """Scheduled notification title, or an empty string when unavailable."""

    body: str = ""
    """Scheduled body text, or an empty string when unavailable."""

    payload: str = ""
    """Application payload stored with the scheduled notification."""


@dataclass
class ActiveNotification:
    """
    Snapshot of a delivered notification that has not been removed.

    Returned by :meth:`flet_notifications.LocalNotifications.get_active_notifications`.
    Availability of individual fields depends on the platform; missing text values
    become empty strings and a missing identifier becomes `0`. Modifying this object
    does not change the notification.
    """

    id: int = 0
    """Native notification identifier, or `0` when unavailable."""

    channel_id: str = ""
    """Android notification-channel ID, or an empty string when unavailable."""

    group_key: str = ""
    """Android notification-group key, or an empty string when unavailable."""

    tag: str = ""
    """Android notification tag, or an empty string when unavailable."""

    title: str = ""
    """Displayed title, or an empty string when unavailable."""

    body: str = ""
    """Displayed body text, or an empty string when unavailable."""

    payload: str = ""
    """Application payload when returned by the platform, otherwise an empty string."""

    big_text: str = ""
    """Expanded Android big-text content, or an empty string when unavailable."""


@dataclass
class LaunchDetails:
    """
    Information about whether a notification launched the application.

    Returned by
    :meth:`flet_notifications.LocalNotifications.get_notification_app_launch_details`.
    This describes the launch of the app, rather than the latest notification received
    while the app was running.
    """

    did_notification_launch_app: bool = False
    """Whether a notification caused the application to launch."""

    notification: NotificationEvent | None = None
    """
    Response associated with the launch, when available.

    Can be `None` when no notification launched the app or the platform cannot provide a
    response. See :class:`flet_notifications.NotificationEvent`.
    """
