from dataclasses import dataclass
from enum import Enum

import flet as ft

__all__ = [
    "NotificationError",
    "NotificationErrorCode",
    "NotificationEvent",
    "ResponseType",
]


class ResponseType(Enum):
    """
    Kinds of notification response represented by
    :class:`flet_notifications.NotificationEvent`.

    :attr:`flet_notifications.NotificationEvent.response_type` contains the string value
    of the enum member, not a :class:`flet_notifications.ResponseType`
    instance.
    """

    TAP = "tap"
    """The user selected the notification itself."""

    ACTION = "action"
    """The user selected one of the notification action buttons."""

    DISMISSED = "dismissed"
    """
    The platform reported that the notification was dismissed.

    Reporting requires native support and configuration. This enum value alone does not
    enable dismissal reporting.
    """


@dataclass
class NotificationEvent(ft.Event[ft.EventControlType]):
    """
    Notification selection, action response, or reported dismissal.

    Delivered to :attr:`flet_notifications.LocalNotifications.on_tap`,
    :attr:`flet_notifications.LocalNotifications.on_action`, and
    :attr:`flet_notifications.LocalNotifications.on_dismissed`. The inherited `control`
    is the service that emitted the event. On Windows, the inherited `data` mapping
    contains action-input values keyed by the input ID.
    """

    id: int = 0
    """Identifier of the notification; native responses without an ID use `-1`."""

    action_id: str = ""
    """
    Selected action's :attr:`flet_notifications.NotificationAction.id`.

    An empty string indicates a body tap or a dismissal rather than an action.
    """

    payload: str = ""
    """
    Application payload supplied when the notification was created.

    An empty string represents no payload. The service does not interpret the payload;
    the application can use it for routing or identifying an item.
    """

    input: str = ""
    """
    Text entered through a notification reply input, or an empty string.

    On Windows, the bridge copies the sole input value here when exactly one input is
    returned. The full Windows input mapping remains in `data`.
    """

    response_type: str = ResponseType.TAP.value
    """
    String response kind: `"tap"`, `"action"`, or `"dismissed"`.

    Compare with :attr:`flet_notifications.ResponseType.TAP` followed by `.value`, for
    example, rather than the enum member itself.
    """
    # Windows action inputs arrive in the inherited `data` field, keyed by
    # the input id (Windows leaves `input` null).


class NotificationErrorCode:
    """
    Machine-readable error codes returned by the notification bridge.

    Compare these constants with :attr:`flet_notifications.NotificationError.code`.
    Codes describe the failing operation or parsing stage; read
    :attr:`flet_notifications.NotificationError.message` for native details. They are
    strings, not enum members.
    """

    UNSUPPORTED_PLATFORM = "unsupported_platform"
    """The operation is not implemented on the current platform."""

    INIT_FAILED = "init_failed"
    """The notification backend could not initialize."""

    SHOW_FAILED = "show_failed"
    """Displaying a notification failed."""

    SCHEDULE_FAILED = "schedule_failed"
    """Scheduling a notification or registering a repeating request failed."""

    INVALID_ACTION = "invalid_action"
    """Action parsing rejected the supplied data."""

    INVALID_SCHEDULE = "invalid_schedule"
    """The schedule time could not be parsed."""

    INVALID_STYLE = "invalid_style"
    """The style discriminator or required style data was invalid."""

    INVALID_CHANNEL = "invalid_channel"
    """A channel declaration was missing its required ID or name."""

    INVALID_SERVICE_ID = "invalid_service_id"
    """
    A foreground-service notification used the forbidden ID `0`.

    The Python method rejects this earlier with `ValueError`.
    """

    INVALID_OPTION = "invalid_option"
    """The bridge rejected an invalid platform option, such as an unknown category."""

    CHANNEL_FAILED = "channel_failed"
    """Creating or querying an Android channel or channel group failed."""

    FOREGROUND_SERVICE_FAILED = "foreground_service_failed"
    """Starting the Android foreground service failed."""

    QUERY_FAILED = "query_failed"
    """A notification query failed or its returned JSON could not be decoded."""

    PERMISSION_FAILED = "permission_failed"
    """
    Reserved code for a failed permission operation.

    Not every native permission failure is translated to this code by the current
    bridge.
    """

    UNKNOWN_METHOD = "unknown_method"
    """The native service did not recognize the invoked method name."""


class NotificationError(ft.FletException):
    """
    Exception raised when the notification bridge returns an error result.

    Inspect :attr:`code` to handle known failures and :attr:`message` for details.
    Native errors not converted to the bridge's error format may propagate through Flet
    separately.

    Args:
        code: Machine-readable error identifier; see
            :class:`flet_notifications.NotificationErrorCode`.
        message: Optional explanation of the failure.
    """

    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        """
        Machine-readable failure code; see
        :class:`flet_notifications.NotificationErrorCode`.
        """
        self.message = message
        """Native failure details, or an empty string when none were supplied."""
        super().__init__(f"{code}: {message}" if message else code)

    def __repr__(self) -> str:
        return f"NotificationError(code={self.code!r}, message={self.message!r})"


def check_result(result: object) -> None:
    """
    Raise :class:`flet_notifications.NotificationError` if a Dart invoke returned an
    error string.

    Dart service methods return `"error:<code>:<message>"` on failure.
    """
    if isinstance(result, str) and result.startswith("error:"):
        _, _, rest = result.partition(":")
        code, _, message = rest.partition(":")
        raise NotificationError(code.strip(), message.strip())


def to_bool(result: object) -> bool:
    """Coerce a Dart invoke result to bool (`"true"`/`"false"`)."""
    check_result(result)
    if isinstance(result, bool):
        return result
    return str(result).strip().lower() == "true"
