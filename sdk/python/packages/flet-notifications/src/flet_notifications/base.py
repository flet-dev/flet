from dataclasses import dataclass
from enum import Enum
from typing import TypeVar

import flet as ft
from flet.utils import from_dict

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

    Note:
        Reporting requires native support and configuration. This enum value alone does
        not enable dismissal reporting.
    """


@dataclass
class NotificationEvent(ft.Event[ft.EventControlType]):
    """
    Notification selection, action response, or reported dismissal.

    Delivered to :attr:`flet_notifications.LocalNotifications.on_tap`,
    :attr:`flet_notifications.LocalNotifications.on_action`, and
    :attr:`flet_notifications.LocalNotifications.on_dismiss`. The inherited `control`
    is the service that emitted the event.

    Note:
        On Windows, the inherited `data` mapping contains reply values keyed by
        :attr:`flet_notifications.NotificationAction.id`. See
        :attr:`flet_notifications.LocalNotifications.on_action` for how to read them.
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

    Note:
        On Windows, contains the reply text when exactly one input value is returned.
        All reply values remain available in the inherited `data` mapping, keyed by
        :attr:`flet_notifications.NotificationAction.id`.
    """

    response_type: str = ResponseType.TAP.value
    """
    String response kind: `"tap"`, `"action"`, or `"dismissed"`.

    Compare with :attr:`flet_notifications.ResponseType.TAP` followed by `.value`, for
    example, rather than the enum member itself.
    """


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
    """A notification query failed or returned malformed data."""

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


_QueryItem = TypeVar("_QueryItem")


def parse_query_list(
    result: object,
    item_type: type[_QueryItem],
    *,
    defaults: dict[str, object] | None = None,
) -> list[_QueryItem]:
    """Reconstruct query snapshots without silently skipping malformed entries."""
    check_result(result)
    if not isinstance(result, list):
        raise NotificationError(
            "query_failed", f"Expected a list of {item_type.__name__}"
        )
    items = []
    for index, entry in enumerate(result):
        if not isinstance(entry, dict):
            raise NotificationError(
                "query_failed",
                f"Expected {item_type.__name__} mapping at index {index}",
            )
        try:
            items.append(from_dict(item_type, {**(defaults or {}), **entry}))
        except (TypeError, ValueError) as exc:
            raise NotificationError(
                "query_failed", f"Invalid {item_type.__name__} at index {index}: {exc}"
            ) from exc
    return items
