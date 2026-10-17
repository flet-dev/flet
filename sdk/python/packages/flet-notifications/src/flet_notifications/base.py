"""Shared types and helpers for flet-notifications."""

from dataclasses import dataclass
from enum import Enum

import flet as ft


class ResponseType(str, Enum):
    """Type of a notification response delivered from the OS to the app."""

    TAP = "tap"
    ACTION = "action"
    DISMISSED = "dismissed"


@dataclass
class NotificationEvent(ft.Event[ft.EventControlType]):
    """A notification tap, action-button press or dismissal.

    Delivered to `on_tap` / `on_action` / `on_dismissed` handlers.
    """

    id: int = 0
    action_id: str = ""  # "" for a plain tap; the button id for actions
    payload: str = ""
    input: str = ""  # inline-reply text, when the action had an input
    response_type: str = ResponseType.TAP.value
    # Windows action inputs arrive in the inherited `data` field, keyed by
    # the input id (Windows leaves `input` null).


class NotificationErrorCode:
    """Stable machine-readable error codes raised by the service."""

    UNSUPPORTED_PLATFORM = "unsupported_platform"
    INIT_FAILED = "init_failed"
    SHOW_FAILED = "show_failed"
    SCHEDULE_FAILED = "schedule_failed"
    INVALID_ACTION = "invalid_action"
    INVALID_SCHEDULE = "invalid_schedule"
    INVALID_STYLE = "invalid_style"
    INVALID_CHANNEL = "invalid_channel"
    INVALID_SERVICE_ID = "invalid_service_id"
    INVALID_OPTION = "invalid_option"
    CHANNEL_FAILED = "channel_failed"
    FOREGROUND_SERVICE_FAILED = "foreground_service_failed"
    QUERY_FAILED = "query_failed"
    PERMISSION_FAILED = "permission_failed"
    UNKNOWN_METHOD = "unknown_method"


class NotificationError(Exception):
    """Raised when a notification operation fails.

    `code` is a stable machine-readable identifier — see
    :class:`NotificationErrorCode` for the full list.
    """

    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}" if message else code)

    def __repr__(self) -> str:
        return f"NotificationError(code={self.code!r}, message={self.message!r})"


def check_result(result: object) -> None:
    """Raise :class:`NotificationError` if a Dart invoke returned an error string.

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
