import dataclasses
from typing import Any

from flet.utils.validation import validate
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
