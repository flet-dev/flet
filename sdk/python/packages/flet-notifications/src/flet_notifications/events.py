from dataclasses import dataclass

import flet as ft

__all__ = [
    "NotificationActionEvent",
    "NotificationEvent",
]


@dataclass(kw_only=True)
class NotificationEvent(ft.Event[ft.EventControlType]):
    """
    The user selected a notification.

    Delivered to :attr:`flet_notifications.Notifications.on_tap`. Action buttons deliver
    :class:`flet_notifications.NotificationActionEvent` instead. The inherited
    `control` is the service that emitted the event.
    """

    id: int | None = None
    """Identifier of the notification, or `None` when the platform reports none."""

    payload: str | None = None
    """
    Application payload supplied when the notification was created.

    `None` when the notification has no payload. The service does not interpret the
    payload; the application can use it for routing or identifying an item.
    """


@dataclass(kw_only=True)
class NotificationActionEvent(NotificationEvent[ft.EventControlType]):
    """
    The user selected one of a notification's action buttons.

    Delivered to :attr:`flet_notifications.Notifications.on_action`.

    Note:
        On Windows, the inherited `data` mapping contains reply values keyed by
        :attr:`flet_notifications.NotificationAction.id`. See
        :attr:`flet_notifications.Notifications.on_action` for how to read them.
    """

    action_id: str
    """Selected action's :attr:`flet_notifications.NotificationAction.id`."""

    input: str | None = None
    """
    Text entered through the action's reply input, or `None` when there is none.

    Note:
        On Windows, contains the reply text when exactly one input value is returned.
        All reply values remain available in the inherited `data` mapping, keyed by
        :attr:`flet_notifications.NotificationAction.id`.
    """
