"""Event payload types delivered from the Dart side."""

from __future__ import annotations

from dataclasses import dataclass

from flet_notifications.base import NotificationEvent


@dataclass
class PendingNotification:
    """A scheduled notification that has not been delivered yet.

    Returned by :meth:`LocalNotifications.get_pending_notifications`.
    """

    id: int
    title: str = ""
    body: str = ""
    payload: str = ""


@dataclass
class ActiveNotification:
    """A notification currently shown in the notification tray."""

    id: int = 0
    channel_id: str = ""
    group_key: str = ""
    tag: str = ""
    title: str = ""
    body: str = ""
    payload: str = ""
    big_text: str = ""


@dataclass
class LaunchDetails:
    """Why/how the app was launched, if a notification launched it."""

    did_notification_launch_app: bool = False
    notification: NotificationEvent | None = None
