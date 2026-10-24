import dataclasses
from typing import Any

import flet as ft
from flet.utils.validation import FieldRule, V, validate
from flet_notifications.base import NotificationInvalidArgumentError

__all__ = []


def validate_arguments(*values: Any) -> None:
    """
    Check method arguments, and the values nested in them, against their rules.

    Rules are the `V` validators in each class's annotations.

    Raises:
        NotificationInvalidArgumentError: For the first value that breaks a rule,
            naming its class.
    """
    for value in values:
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            try:
                validate(value)
            except ValueError as e:
                raise NotificationInvalidArgumentError(
                    f"{type(value).__name__}: {e}"
                ) from None
            validate_arguments(
                *(getattr(value, f.name) for f in dataclasses.fields(value))
            )
        elif isinstance(value, (list, tuple)):
            validate_arguments(*value)
        elif isinstance(value, dict):
            validate_arguments(*value.values())


def validate_notification_id(id: int) -> None:
    """
    Check that `id` fits the 32-bit signed integer platforms identify
    notifications with.

    Raises:
        NotificationInvalidArgumentError: If `id` is outside the range of a
            32-bit signed integer.
    """
    if not -(2**31) <= id <= 2**31 - 1:
        raise NotificationInvalidArgumentError(
            f"id must be between {-(2**31)} and {2**31 - 1}, got {id}"
        )


def validate_non_empty(**values: str) -> None:
    """
    Check that string arguments aren't empty.

    Raises:
        NotificationInvalidArgumentError: Naming the first empty argument.
    """
    for name, value in values.items():
        if not value:
            raise NotificationInvalidArgumentError(f"{name} must be non-empty")


def non_negative_duration(*special: int) -> FieldRule:
    """
    A `V` rule requiring a `DurationValue` field not to be negative.

    Args:
        special: Negative values, in milliseconds, the field also accepts, such
            as `-1` for a platform default.
    """

    def check(instance: Any, field_name: str, value: Any) -> None:
        if value is None:
            return
        milliseconds = (
            value.in_milliseconds if isinstance(value, ft.Duration) else value
        )
        if milliseconds < 0 and milliseconds not in special:
            allowed = "".join(f", except {s}" for s in special)
            raise ValueError(
                f"{field_name} must not be negative{allowed}, got {milliseconds} ms"
            )

    return V.field(check)
