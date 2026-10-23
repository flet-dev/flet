from dataclasses import dataclass
from typing import TypeVar

import flet as ft
from flet.utils import from_dict

__all__ = [
    "NotificationActionEvent",
    "NotificationError",
    "NotificationEvent",
    "NotificationInitializationError",
    "NotificationInvalidArgumentError",
    "NotificationPermissionError",
    "NotificationUnsupportedPlatformError",
]


@dataclass(kw_only=True)
class NotificationEvent(ft.Event[ft.EventControlType]):
    """
    The user selected a notification, or the platform reported its dismissal.

    Delivered to :attr:`flet_notifications.LocalNotifications.on_tap` and
    :attr:`flet_notifications.LocalNotifications.on_dismiss`. Action buttons deliver
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

    Delivered to :attr:`flet_notifications.LocalNotifications.on_action`.

    Note:
        On Windows, the inherited `data` mapping contains reply values keyed by
        :attr:`flet_notifications.NotificationAction.id`. See
        :attr:`flet_notifications.LocalNotifications.on_action` for how to read them.
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


class NotificationError(ft.FletException):
    """
    Base class for notification failures.

    Raised as-is when the platform reports a failure without a more specific class,
    with a message starting with the platform's own error code, such as
    `"invalid_icon: ..."` when a notification icon resource is missing. Catch it to
    handle every notification failure.

    See these subclasses:

    - :class:`~flet_notifications.NotificationUnsupportedPlatformError`
    - :class:`~flet_notifications.NotificationInitializationError`
    - :class:`~flet_notifications.NotificationInvalidArgumentError`
    - :class:`~flet_notifications.NotificationPermissionError`
    """


class NotificationUnsupportedPlatformError(
    NotificationError, ft.FletUnsupportedPlatformException
):
    """
    Raised when an operation is not available on the current platform.

    For example, :meth:`flet_notifications.LocalNotifications.start_foreground_service`
    outside Android. Also caught as :class:`flet.FletUnsupportedPlatformException`.
    """


class NotificationInitializationError(NotificationError):
    """
    Raised when the notification backend could not initialize.

    The message describes the cause. Call
    :meth:`flet_notifications.LocalNotifications.initialize` to retry.
    """


class NotificationInvalidArgumentError(NotificationError, ValueError):
    """
    Raised when a value passed to a notification operation is invalid.

    Also caught as `ValueError`.
    """


class NotificationPermissionError(NotificationError):
    """
    Raised when the platform refuses an operation for lack of permission.

    For example, scheduling with an exact
    :class:`~flet_notifications.AndroidScheduleMode` without exact-alarm access; see
    :meth:`flet_notifications.LocalNotifications.request_exact_alarm_permission`.
    """


_BRIDGE_ERRORS: dict[str, type[NotificationError]] = {
    "unsupported_platform": NotificationUnsupportedPlatformError,
    "initialization_failed": NotificationInitializationError,
    "invalid_argument": NotificationInvalidArgumentError,
    "permission_denied": NotificationPermissionError,
    "operation_failed": NotificationError,
}
"""Exception class for each failure code the Dart service reports."""


def error_from_bridge(text: str) -> NotificationError:
    """
    Rebuild a bridge failure from the text Flet reports for a failed method call.

    The Dart service fails with `"<code>: <message>"`. Other failures, such as a
    missing control, become a plain :class:`flet_notifications.NotificationError`.
    """
    code, separator, message = text.partition(": ")
    error = _BRIDGE_ERRORS.get(code) if separator else None
    return error(message) if error else NotificationError(text)


_QueryItem = TypeVar("_QueryItem")


def parse_query_list(
    result: object,
    item_type: type[_QueryItem],
) -> list[_QueryItem]:
    """Reconstruct query snapshots without silently skipping malformed entries."""
    if not isinstance(result, list):
        raise NotificationError(
            f"Expected a list of {item_type.__name__}",
        )
    items = []
    for index, entry in enumerate(result):
        if not isinstance(entry, dict):
            raise NotificationError(
                f"Expected {item_type.__name__} mapping at index {index}",
            )
        try:
            items.append(from_dict(item_type, entry))
        except (TypeError, ValueError) as exc:
            raise NotificationError(
                f"Invalid {item_type.__name__} at index {index}: {exc}",
            ) from exc
    return items
