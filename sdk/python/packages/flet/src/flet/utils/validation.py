"""
Validation helpers for dataclass-style models, including Flet controls.

This module provides composable rule objects that are attached to annotated
fields (`typing.Annotated`) and to class-level cross-field declarations
(`__validation_rules__`).

Primary use cases:
1. Generic dataclass/domain model validation via direct `validate(instance)` calls.
2. Flet outbound validation, where `BaseControl` invokes `validate(self)`
   before patch serialization so the invalid state fails on Python side first.
"""

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from typing import (
    Annotated,
    Any,
    Callable,
    ClassVar,
    Optional,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from flet.utils.deprecated import deprecated_warning

__all__ = [
    "ClassRule",
    "FieldRule",
    "V",
    "ValidationDeclarationError",
    "ValidationRules",
    "validate",
]

FieldCheck = Callable[[Any, str, Any], None]
FieldMessage = Union[str, Callable[[Any, str, Any], str]]
ClassCheck = Callable[[Any], None]
ClassMessage = Union[str, Callable[[Any], str]]
ClassPredicate = Callable[[Any], bool]


class ValidationDeclarationError(RuntimeError):
    """
    Raised when a validation rule declaration is invalid.

    This is intended for those declaring validation rules,
    not for end-user value input validation failures.
    """


@dataclass(frozen=True)
class FieldRule:
    """A single validation rule applied to one annotated field value."""

    _check: FieldCheck

    def validate(self, instance: Any, field_name: str, value: Any) -> None:
        """Validate one field value for a specific class instance."""
        self._check(instance, field_name, value)


@dataclass(frozen=True)
class ClassRule:
    """A cross-field validation rule evaluated against one class instance."""

    _check: ClassCheck

    def validate(self, instance: Any) -> None:
        """Validate one class instance."""
        self._check(instance)


ValidationRules = ClassVar[tuple[ClassRule, ...]]
"""Alias for class-level `__validation_rules__` declarations."""


@dataclass(frozen=True)
class _ClassValidationSpec:
    """Compiled validation specification for one class."""

    field_rules: tuple[tuple[str, FieldRule], ...]
    class_rules: tuple[ClassRule, ...]


_DEPRECATED_WARNINGS_KEY = "__deprecated_validation_warnings"


def _get_warned_deprecated_fields(instance: Any) -> Optional[set[str]]:
    """
    Return a mutable set of already-emitted deprecation warning keys.

    Warnings are tracked on a private runtime attribute so they do not leak into
    serialized control data.
    """

    warned = getattr(instance, _DEPRECATED_WARNINGS_KEY, None)
    if warned is not None:
        return warned

    warned = set()
    try:
        setattr(instance, _DEPRECATED_WARNINGS_KEY, warned)
    except Exception:
        return None
    return warned


def _resolve_field_message(
    message: FieldMessage, instance: Any, field_name: str, value: Any
) -> str:
    """Render a field-level message that may be static text or a callable."""
    if callable(message):
        return message(instance, field_name, value)
    return message


def _resolve_class_message(message: ClassMessage, instance: Any) -> str:
    """Render a class-level message that may be static text or a callable."""
    if callable(message):
        return message(instance)
    return message


def _format_expected_type(
    expected_type: Union[type[Any], tuple[type[Any], ...]],
) -> str:
    """Format expected type(s) into a readable sentence fragment."""
    if not isinstance(expected_type, tuple):
        return expected_type.__name__
    names = [t.__name__ for t in expected_type]
    if len(names) == 0:
        return "unknown"
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} or {names[1]}"
    return f"{', '.join(names[:-1])}, or {names[-1]}"


def _format_allowed_values(values: tuple[Any, ...]) -> str:
    """Format allowed values into a readable sentence fragment."""
    value_names = [repr(value) for value in values]
    if len(value_names) == 1:
        return value_names[0]
    if len(value_names) == 2:
        return f"{value_names[0]} or {value_names[1]}"
    return f"{', '.join(value_names[:-1])}, or {value_names[-1]}"


class V:
    """
    Validation rule builder namespace.

    Methods return `FieldRule` or `ClassRule` instances which are attached to
    class fields (`Annotated[...]`) or class-level `__validation_rules__`.
    """

    @staticmethod
    def field(check: FieldCheck) -> FieldRule:
        """Wrap a custom field validator callback into a `FieldRule`."""
        return FieldRule(check)

    @staticmethod
    def deprecated(
        replacement: Optional[str] = None,
        *,
        reason: Optional[str] = None,
        version: str,
        delete_version: Optional[str] = None,
    ) -> FieldRule:
        """
        Emit a one-time deprecation warning when a field value is set.

        This rule is intended for soft-deprecating dataclass/control properties
        without changing value flow. It does not mutate field values.

        Args:
            replacement: Optional preferred property name used in default message.
            reason: Optional full deprecation reason. When omitted, a replacement-
                based message is generated.
            version: Version where deprecation starts.
            delete_version: Optional version where removal is planned.
        """

        default_reason = (
            f"Use `{replacement}` instead."
            if replacement is not None
            else "This property is deprecated."
        )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if value is None:
                return

            warning_key = f"{instance.__class__.__name__}.{field_name}"
            warned = _get_warned_deprecated_fields(instance)
            if warned is not None and warning_key in warned:
                return

            deprecated_warning(
                name=warning_key,
                reason=reason or default_reason,
                version=version,
                delete_version=delete_version,
                type="property",
            )
            if warned is not None:
                warned.add(warning_key)

        return FieldRule(_check)

    @staticmethod
    def ensure(
        predicate: ClassPredicate,
        *,
        message: Optional[ClassMessage] = None,
    ) -> ClassRule:
        """
        Build a generic cross-field predicate rule.

        When `message` is omitted, a generic fallback is used.
        """

        def _check(instance: Any) -> None:
            if not predicate(instance):
                if message is not None:
                    raise ValueError(_resolve_class_message(message, instance))
                predicate_name = getattr(predicate, "__name__", None)
                if predicate_name and predicate_name != "<lambda>":
                    raise ValueError(f"Validation failed: {predicate_name}")
                raise ValueError("Validation failed.")

        return ClassRule(_check)

    @staticmethod
    def instance_of(
        expected_type: Union[type[Any], tuple[type[Any], ...]],
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate a field value type with an optional custom error message.

        Property docstring Raises wording: `If it is not of type ...`.

        Args:
            expected_type: Allowed runtime type(s).
            message: Optional custom error message/template.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if value is None and _resolve_allow_none_for_field(
                instance.__class__, field_name
            ):
                return
            if not isinstance(value, expected_type):
                if message is None:
                    raise ValueError(
                        f"{field_name} must be of type "
                        f"{_format_expected_type(expected_type)}, got {type(value)}"
                    )
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )

        return FieldRule(_check)

    @staticmethod
    def visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is visible, i.e. `Control.visible` is `True`.

        Property docstring Raises wording: `If it is not visible.`

        Args:
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: f"{field_name} must be visible",
            ):
                return
            if getattr(value, "visible", False):
                return
            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )
            raise ValueError(f"{field_name} must be visible")

        return FieldRule(_check)

    @staticmethod
    def visible_controls(
        *,
        min_count: int,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field contains at least `min_count` visible controls.

        Property docstring Raises wording:
        - `If it does not contain at least one visible Control.`
        - `If it does not contain at least n visible Controls.`

        The field value is expected to be an iterable of controls exposing a
        `visible` boolean attribute.

        Args:
            min_count: Minimum number of visible controls required.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `min_count` is not greater than or
                equal to `1`.
        """
        if min_count < 1:
            raise ValidationDeclarationError(
                f"min_count must be greater than or equal to 1, got {min_count}"
            )

        def _default_error(field_name: str, visible_count: int) -> str:
            if min_count == 1:
                return (
                    f"{field_name} must contain at least one visible Control, "
                    f"got {visible_count}"
                )
            return (
                f"{field_name} must contain at least {min_count} visible Controls, "
                f"got {visible_count}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: _default_error(field_name, 0),
            ):
                return

            try:
                visible_count = sum(
                    1 for item in value if getattr(item, "visible", False)
                )
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(_default_error(field_name, 0)) from err

            if visible_count < min_count:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(_default_error(field_name, visible_count))

        return FieldRule(_check)

    @staticmethod
    def str_or_visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is either a string or a visible instance.

        Property docstring Raises wording:
        `If it is neither a string nor a visible Control.`

        Args:
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must be a string or a visible Control"
                ),
            ):
                return
            if isinstance(value, str) or getattr(value, "visible", False):
                return
            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )
            raise ValueError(f"{field_name} must be a string or a visible Control")

        return FieldRule(_check)

    @staticmethod
    def gt(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value > bound`.

        Property docstring Raises wording:
        `If it is not strictly greater than ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be strictly greater than {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value <= bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be strictly greater than {bound}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def ge(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value >= bound`.

        Property docstring Raises wording:
        `If it is not greater than or equal to ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be greater than or equal to {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value < bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be greater than or equal to {bound}, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def lt(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value < bound`.

        Property docstring Raises wording:
        `If it is not strictly less than ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be less than {bound}, got {current_value}"
                ),
            ):
                return
            if value >= bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(f"{field_name} must be less than {bound}, got {value}")

        return FieldRule(_check)

    @staticmethod
    def le(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value <= bound`.

        Property docstring Raises wording:
        `If it is not less than or equal to ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be less than or equal to {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value > bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be less than or equal to {bound}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def between(
        minimum: Any,
        maximum: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `minimum <= value <= maximum`.

        Property docstring Raises wording:
        `If it is not between ... and ..., inclusive.`
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be between {minimum} and {maximum} inclusive, "
                    f"got {current_value}"
                ),
            ):
                return
            if not (minimum <= value <= maximum):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be between {minimum} and {maximum} inclusive, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def factor_of(
        base: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is an integer factor of `base`.

        Property docstring Raises wording:
        `If it is not a factor of ...`.

        This rule is sign-neutral. To enforce direction, compose with:
        - `V.gt(0)` for positive factors, or
        - `V.lt(0)` for negative factors.

        Args:
            base: The integer that validated values must evenly divide.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `base` is zero or not an integer.
        """
        if not isinstance(base, int) or isinstance(base, bool) or base == 0:
            raise ValidationDeclarationError(
                f"base must be a non-zero integer, got {base!r}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be a factor of {base}, got {current_value}"
                ),
            ):
                return
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value == 0
                or base % value != 0
            ):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be a factor of {base}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def multiple_of(
        divisor: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is an integer multiple of `divisor`.

        Property docstring Raises wording:
        `If it is not a multiple of ...`.

        This rule is sign-neutral. To enforce direction, compose with:
        - `V.gt(0)` for positive multiples, or
        - `V.lt(0)` for negative multiples.

        Args:
            divisor: Divisor used for the divisibility check.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `divisor` is zero or not an integer.
        """
        if not isinstance(divisor, int) or isinstance(divisor, bool) or divisor == 0:
            raise ValidationDeclarationError(
                f"divisor must be a non-zero integer, got {divisor!r}"
            )
        normalized_divisor = abs(divisor)

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be a multiple of {normalized_divisor}, "
                    f"got {current_value}"
                ),
            ):
                return
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value % normalized_divisor != 0
            ):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be a multiple of {normalized_divisor}, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def eq(
        expected: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value == expected`.

        Property docstring Raises wording:
        `If it is not equal to ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be equal to {expected}, got {current_value}"
                ),
            ):
                return
            if value != expected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be equal to {expected}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def ne(
        unexpected: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value != unexpected`.

        Property docstring Raises wording:
        `If it is equal to ...`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must not be equal to {unexpected}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value == unexpected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must not be equal to {unexpected}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def one_of(
        allowed_values: Iterable[Any],
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that `value` belongs to a fixed set of allowed values.

        Property docstring Raises wording:
        `If it is not one of ...`.

        Args:
            allowed_values: Allowed values collection.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `allowed_values` is empty.
        """
        allowed_values_tuple = tuple(allowed_values)
        if len(allowed_values_tuple) == 0:
            raise ValidationDeclarationError(
                "allowed_values must contain at least one value"
            )

        allowed_values_text = _format_allowed_values(allowed_values_tuple)

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be one of {allowed_values_text}, "
                    f"got {current_value!r}"
                ),
            ):
                return
            if value not in allowed_values_tuple:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be one of {allowed_values_text}, got {value!r}"
                )

        return FieldRule(_check)

    @staticmethod
    def or_(
        *rules: FieldRule,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that at least one field rule passes.

        Args:
            rules: Field rules evaluated in declaration order.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If no rules are provided.
            ValidationDeclarationError: If any provided object is not a
                `FieldRule`.
        """
        if len(rules) == 0:
            raise ValidationDeclarationError("or_ requires at least one field rule")
        for rule in rules:
            if not isinstance(rule, FieldRule):
                raise ValidationDeclarationError("or_ expects only FieldRule instances")

        def _check(instance: Any, field_name: str, value: Any) -> None:
            errors: list[str] = []
            for rule in rules:
                try:
                    rule.validate(instance, field_name, value)
                    return
                except ValueError as err:
                    errors.append(str(err))

            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )

            if len(errors) == 1:
                raise ValueError(errors[0])

            joined_errors = "; or ".join(errors)
            raise ValueError(
                f"{field_name} must satisfy at least one of the allowed "
                f"conditions: {joined_errors}"
            )

        return FieldRule(_check)

    @staticmethod
    def non_empty(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field value is non-empty (`len(value) > 0`).

        Property docstring Raises wording:
        `If it is empty.`
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must be a non-empty sized value, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a non-empty sized value, got {type(value)}"
                ) from err

            if length == 0:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(f"{field_name} must be non-empty")

        return FieldRule(_check)

    @staticmethod
    def length_ge(
        minimum: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field has length greater than or equal to `minimum`.

        Property docstring Raises wording:
        `If its length is less than ...`.

        Args:
            minimum: Inclusive minimum allowed length.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `minimum` is negative.
        """
        if minimum < 0:
            raise ValidationDeclarationError(
                f"minimum must be greater than or equal to 0, got {minimum}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length greater than or equal to "
                    f"{minimum}, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length greater than "
                    f"or equal to {minimum}, got {type(value)}"
                ) from err

            if length < minimum:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length greater than or equal to "
                    f"{minimum}, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def length_eq(
        expected: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field has length equal to `expected`.

        Property docstring Raises wording:
        `If its length is not equal to ...`.

        Args:
            expected: Required length.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `expected` is negative.
        """
        if expected < 0:
            raise ValidationDeclarationError(
                f"expected must be greater than or equal to 0, got {expected}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length equal to {expected}, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length equal to "
                    f"{expected}, got {type(value)}"
                ) from err

            if length != expected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length equal to {expected}, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def length_between(
        minimum: int,
        maximum: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field length is between bounds, inclusive.

        Property docstring Raises wording:
        `If its length is not between ... and ..., inclusive.`

        Args:
            minimum: Inclusive minimum allowed length.
            maximum: Inclusive maximum allowed length.
            message: Optional custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `minimum` is negative.
            ValidationDeclarationError: If `maximum` is less than `minimum`.
        """
        if minimum < 0:
            raise ValidationDeclarationError(
                f"minimum must be greater than or equal to 0, got {minimum}"
            )
        if maximum < minimum:
            raise ValidationDeclarationError(
                f"maximum must be greater than or equal to minimum ({minimum}), "
                f"got {maximum}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length between {minimum} and {maximum} "
                    f"inclusive, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length between "
                    f"{minimum} and {maximum} inclusive, got {type(value)}"
                ) from err

            if not (minimum <= length <= maximum):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length between {minimum} and {maximum} "
                    f"inclusive, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def gt_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name > other_field` on an instance.

        Property docstring Raises wording:
        `If it is not strictly greater than [\`other_field\`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field on the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be strictly greater than "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value <= other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be strictly greater than "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def ge_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name >= other_field` on an instance.

        Property docstring Raises wording:
        `If it is not greater than or equal to [\`other_field\`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field on the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be greater than or equal to "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value < other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be greater than or equal to "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def lt_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name < other_field` on an instance.

        Property docstring Raises wording:
        `If it is not strictly less than [\`other_field\`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field on the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be strictly less than "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value >= other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be strictly less than "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def le_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name <= other_field` on an instance.

        Property docstring Raises wording:
        `If it is not less than or equal to [\`other_field\`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field on the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be less than or equal to "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value > other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be less than or equal to "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)


def _get_declared_type_hints(cls: type[Any]) -> dict[str, Any]:
    """
    Resolve declared annotations for one class with best-effort extras support.

    Only annotations declared directly on `cls` are returned. This allows MRO-based
    merging in `_compile_class_spec()` without duplicating inherited members.
    """

    annotations = getattr(cls, "__annotations__", {})
    if not annotations:
        return {}

    module = sys.modules.get(cls.__module__)
    globalns = module.__dict__ if module else None
    try:
        type_hints = get_type_hints(cls, globalns=globalns, include_extras=True)
    except TypeError:
        type_hints = get_type_hints(cls, globalns=globalns)
    except Exception:
        type_hints = annotations

    return {name: type_hints.get(name, hint) for name, hint in annotations.items()}


@cache
def _get_effective_type_hints(cls: type[Any]) -> dict[str, Any]:
    """
    Resolve effective annotations for `cls`, including inherited fields.

    The result is used for Optional/None inference in field-level rules.
    """

    module = sys.modules.get(cls.__module__)
    globalns = module.__dict__ if module else None
    try:
        return get_type_hints(cls, globalns=globalns, include_extras=True)
    except TypeError:
        return get_type_hints(cls, globalns=globalns)
    except Exception:
        hints: dict[str, Any] = {}
        for base in reversed(cls.__mro__):
            hints.update(getattr(base, "__annotations__", {}))
        return hints


def _strip_annotated(annotation: Any) -> Any:
    """
    Remove `Annotated[...]` wrapper(s), returning the core annotation type.
    """

    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


def _annotation_allows_none(annotation: Any) -> bool:
    """
    Return `True` if annotation contains `None` (for example `Optional[T]`).
    """

    annotation = _strip_annotated(annotation)
    origin = get_origin(annotation)
    if origin is Union:
        return any(arg is type(None) for arg in get_args(annotation))
    return False


def _resolve_allow_none_for_field(model_cls: type[Any], field_name: str) -> bool:
    """
    Resolve `None` allowance for an annotated field on a class.
    """
    annotation = _get_effective_type_hints(model_cls).get(field_name)
    if annotation is None:
        return False
    return _annotation_allows_none(annotation)


def _prepare_field_value(
    instance: Any,
    field_name: str,
    value: Any,
    message: Optional[FieldMessage],
    default_error: Callable[[Any], str],
) -> bool:
    """
    Normalize `None` handling for field-level validators.

    Returns:
        `True` when validation should be skipped because `None` is allowed.
    """

    none_allowed = _resolve_allow_none_for_field(instance.__class__, field_name)
    if value is None and none_allowed:
        return True

    if value is None:
        if message is not None:
            raise ValueError(
                _resolve_field_message(message, instance, field_name, value)
            )
        raise ValueError(default_error(value))

    return False


def _prepare_field_comparison_values(
    instance: Any,
    field_name: str,
    value: Any,
    other_field: str,
    message: Optional[FieldMessage],
    default_error: Callable[[Any, Any], str],
) -> tuple[Any, bool]:
    """
    Load and normalize values for a field-vs-field comparison rule.

    Returns:
        `(other_value, skip_validation)`.
    """

    other_value = getattr(instance, other_field)
    current_none_allowed = _resolve_allow_none_for_field(instance.__class__, field_name)
    other_none_allowed = _resolve_allow_none_for_field(instance.__class__, other_field)

    if value is None and current_none_allowed:
        return other_value, True
    if other_value is None and other_none_allowed:
        return other_value, True

    if value is None or other_value is None:
        if message is not None:
            raise ValueError(
                _resolve_field_message(message, instance, field_name, value)
            )
        raise ValueError(default_error(value, other_value))

    return other_value, False


@cache
def _compile_class_spec(model_cls: type[Any]) -> _ClassValidationSpec:
    """
    Compile and cache effective validation rules for one class.

    Rules are merged in MRO order (base to derived) so subclasses can extend
    validation behavior deterministically.
    """

    field_rules: list[tuple[str, FieldRule]] = []
    class_rules: list[ClassRule] = []

    for cls in reversed(model_cls.__mro__):
        if cls is object:
            continue

        # Collect field-level rules from Annotated metadata.
        for field_name, hint in _get_declared_type_hints(cls).items():
            if get_origin(hint) is Annotated:
                for metadata in get_args(hint)[1:]:
                    if isinstance(metadata, FieldRule):
                        field_rules.append((field_name, metadata))

        # Collect class-level cross-field rules.
        rules = cls.__dict__.get("__validation_rules__", ())
        if rules:
            for rule in rules:
                if isinstance(rule, ClassRule):
                    class_rules.append(rule)

    return _ClassValidationSpec(tuple(field_rules), tuple(class_rules))


def validate(instance: Any) -> None:
    """
    Run all compiled validators for one instance.

    Field rules are evaluated first, then class-level rules.
    Validation stops at the first raised exception.
    """

    spec = _compile_class_spec(instance.__class__)
    for field_name, rule in spec.field_rules:
        rule.validate(instance, field_name, getattr(instance, field_name))
    for rule in spec.class_rules:
        rule.validate(instance)
