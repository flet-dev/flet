from dataclasses import dataclass

__all__ = [
    "ActiveNotification",
    "PendingNotification",
]


@dataclass
class PendingNotification:
    """
    Notification scheduled for future delivery.

    Returned by
    :meth:`flet_notifications.Notifications.get_pending_notifications`. This is a
    query snapshot, not an editable schedule; changing its fields does not update or
    cancel the native request. Unavailable values are `None`.
    """

    id: int
    """Identifier supplied when scheduling the notification."""

    title: str | None = None
    """Scheduled notification title, or `None` when unavailable."""

    body: str | None = None
    """Scheduled body text, or `None` when unavailable."""

    payload: str | None = None
    """Application payload stored with the scheduled notification, if any."""


@dataclass
class ActiveNotification:
    """
    Snapshot of a delivered notification that has not been removed.

    Returned by :meth:`flet_notifications.Notifications.get_active_notifications`.
    Availability of individual fields depends on the platform; unavailable values are
    `None`. Modifying this object does not change the notification.
    """

    id: int | None = None
    """Native notification identifier, or `None` when unavailable."""

    channel_id: str | None = None
    """Android notification-channel ID, or `None` when unavailable."""

    group_key: str | None = None
    """
    Android :attr:`flet_notifications.AndroidGroup.key`, or `None` when unavailable.
    """

    tag: str | None = None
    """Android notification tag, or `None` when unavailable."""

    title: str | None = None
    """Displayed title, or `None` when unavailable."""

    body: str | None = None
    """Displayed body text, or `None` when unavailable."""

    payload: str | None = None
    """Application payload when returned by the platform, otherwise `None`."""

    big_text: str | None = None
    """Expanded Android big-text content, or `None` when unavailable."""
