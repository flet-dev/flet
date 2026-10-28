import flet as ft

__all__ = [
    "NotificationException",
    "NotificationInitializationException",
    "NotificationInvalidArgumentException",
    "NotificationPermissionException",
    "NotificationUnsupportedPlatformException",
]


class NotificationException(ft.FletException):
    """
    Base class for notification failures.

    Raised as-is when the platform reports a failure without a more specific class,
    with a message starting with the platform's own error code, such as
    `"invalid_icon: ..."` when a notification icon resource is missing. Catch it to
    handle every notification failure.

    See these subclasses:

    - :class:`~flet_notifications.NotificationUnsupportedPlatformException`
    - :class:`~flet_notifications.NotificationInitializationException`
    - :class:`~flet_notifications.NotificationInvalidArgumentException`
    - :class:`~flet_notifications.NotificationPermissionException`
    """


class NotificationUnsupportedPlatformException(
    NotificationException, ft.FletUnsupportedPlatformException
):
    """
    Raised when an operation is not available on the current platform.

    For example, :meth:`flet_notifications.Notifications.start_foreground_service`
    outside Android. Also caught as :class:`flet.FletUnsupportedPlatformException`.
    """


class NotificationInitializationException(NotificationException):
    """
    Raised when the notification backend could not initialize.

    The message describes the cause. The service retries the initialization on the
    next method call.
    """


class NotificationInvalidArgumentException(NotificationException, ValueError):
    """
    Raised when a value passed to a notification operation is invalid.

    Also caught as `ValueError`.
    """


class NotificationPermissionException(NotificationException):
    """
    Raised when the platform refuses an operation for lack of permission.

    For example, scheduling with an exact
    :class:`~flet_notifications.AndroidScheduleMode` without exact-alarm access; see
    :meth:`flet_notifications.Notifications.request_exact_alarm_permission`.
    """


_BRIDGE_ERRORS: dict[str, type[NotificationException]] = {
    "unsupported_platform": NotificationUnsupportedPlatformException,
    "initialization_failed": NotificationInitializationException,
    "invalid_argument": NotificationInvalidArgumentException,
    "permission_denied": NotificationPermissionException,
    "operation_failed": NotificationException,
}
"""Exception class for each failure code the Dart service reports."""


def error_from_bridge(text: str) -> NotificationException:
    """
    Rebuild a bridge failure from the text Flet reports for a failed method call.

    The Dart service fails with `"<code>: <message>"`. Other failures, such as a
    missing control, become a plain :class:`flet_notifications.NotificationException`.
    """
    code, separator, message = text.partition(": ")
    error = _BRIDGE_ERRORS.get(code) if separator else None
    return error(message) if error else NotificationException(text)
